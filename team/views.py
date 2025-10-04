from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model

# Import models and utilities from the workspace app
from workspace.models import (
    Workspace, Membership, ActivityLog,
    Group, GroupMembership
)
from .forms import (
    InviteForm, RoleAssignmentForm,
    GroupForm, GroupMembershipForm
)
from workspace.decorators import workspace_required, workspace_admin_required

User = get_user_model()


@login_required
@workspace_required
def team_management(request, workspace_id):
    """
    Main team management page - shows all workspace members
    """
    workspace = get_object_or_404(Workspace, id=workspace_id)
    
    # Get all memberships for this workspace
    memberships = Membership.objects.filter(workspace=workspace).select_related('user')
    
    # Get current user's membership for permission checks
    user_membership = Membership.objects.get(user=request.user, workspace=workspace)
    
    context = {
        'workspace': workspace,
        'memberships': memberships,
        'user_membership': user_membership,
    }
    
    return render(request, 'team/team.html', context)


@login_required
@workspace_admin_required
def invite_member(request, workspace_id):
    """
    Invite new members to workspace via email
    """
    workspace = get_object_or_404(Workspace, id=workspace_id)
    
    if request.method == 'POST':
        form = InviteForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            role = form.cleaned_data['role']
            
            # Check if user exists in system
            try:
                user = User.objects.get(email=email)
                
                # Check if user is already a member
                if Membership.objects.filter(user=user, workspace=workspace).exists():
                    messages.warning(request, f"{email} is already a member of this workspace")
                else:
                    # Add user to workspace
                    Membership.objects.create(
                        user=user,
                        workspace=workspace,
                        role=role
                    )
                    
                    # Log activity
                    ActivityLog.objects.create(
                        workspace=workspace,
                        user=request.user,
                        action=f"invited {user.username} as {role}"
                    )
                    
                    messages.success(request, f"Successfully added {user.username} to the workspace")
                    
            except User.DoesNotExist:
                # User doesn't exist in system - send invitation email
                invitation_link = f"{settings.SITE_URL}/workspace/{workspace.id}/"
                
                # Send invitation email
                send_mail(
                    f"Invitation to join {workspace.name} on PickTask",
                    f"You've been invited to join {workspace.name} on PickTask. "
                    f"Sign up at {settings.SITE_URL}/auth/register/ and then visit {invitation_link}",
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False,
                )
                
                messages.success(
                    request, 
                    f"Invitation sent to {email}. They'll need to register first."
                )
                
                # Log activity
                ActivityLog.objects.create(
                    workspace=workspace,
                    user=request.user,
                    action=f"sent invitation to {email} as {role}"
                )
            
            return redirect('team:team', workspace_id=workspace_id)
    else:
        form = InviteForm()
    
    context = {
        'workspace': workspace,
        'form': form,
    }
    return render(request, 'team/invite.html', context)


@login_required
@workspace_admin_required
def edit_role(request, workspace_id, membership_id):
    """
    Edit a member's role in the workspace
    """
    workspace = get_object_or_404(Workspace, id=workspace_id)
    membership = get_object_or_404(Membership, id=membership_id, workspace=workspace)
    
    # Prevent users from editing their own admin status (optional safety)
    if membership.user == request.user:
        messages.error(request, "You cannot change your own role")
        return redirect('team:team', workspace_id=workspace_id)
    
    if request.method == 'POST':
        form = RoleAssignmentForm(request.POST, instance=membership)
        if form.is_valid():
            form.save()
            
            # Log activity
            ActivityLog.objects.create(
                workspace=workspace,
                user=request.user,
                action=f"updated {membership.user.username}'s role to {membership.get_role_display()}"
            )
            
            messages.success(request, f"Updated {membership.user.username}'s role to {membership.get_role_display()}")
            return redirect('team:team', workspace_id=workspace_id)
    else:
        form = RoleAssignmentForm(instance=membership)
    
    context = {
        'workspace': workspace,
        'membership': membership,
        'form': form,
    }
    return render(request, 'team/roles.html', context)


@login_required
@workspace_admin_required
def remove_member(request, workspace_id, membership_id):
    """
    Remove a member from workspace (admin only)
    """
    workspace = get_object_or_404(Workspace, id=workspace_id)
    membership = get_object_or_404(Membership, id=membership_id, workspace=workspace)
    
    # Prevent users from removing themselves
    if membership.user == request.user:
        messages.error(request, "You cannot remove yourself from the workspace")
        return redirect('team:team', workspace_id=workspace_id)
    
    # Prevent removing the last admin
    admin_count = Membership.objects.filter(workspace=workspace, role='admin').count()
    if membership.role == 'admin' and admin_count <= 1:
        messages.error(request, "Cannot remove the last admin from workspace")
        return redirect('team:team', workspace_id=workspace_id)
    
    user_email = membership.user.email
    membership.delete()
    
    # Log activity
    ActivityLog.objects.create(
        workspace=workspace,
        user=request.user,
        action=f"removed {user_email} from workspace"
    )
    
    messages.success(request, f"Removed {user_email} from workspace")
    return redirect('team:team', workspace_id=workspace_id)


@login_required
@workspace_required
def groups(request, workspace_id):
    """
    Group management - list all groups and handle creation
    """
    workspace = get_object_or_404(Workspace, id=workspace_id)
    groups_list = Group.objects.filter(workspace=workspace).prefetch_related('memberships__user')
    
    # Get current user's membership for permission checks
    user_membership = Membership.objects.get(user=request.user, workspace=workspace)
    
    if request.method == 'POST':
        if user_membership.role != 'admin':
            messages.error(request, "Only admins can create groups.")
            return redirect('team:groups', workspace_id=workspace_id)
            
        form = GroupForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.workspace = workspace
            group.created_by = request.user
            group.save()
            
            # Log activity
            ActivityLog.objects.create(
                workspace=workspace,
                user=request.user,
                action=f"created group '{group.name}'"
            )
            
            messages.success(request, f"Group '{group.name}' created successfully!")
            return redirect('team:groups', workspace_id=workspace_id)
    else:
        form = GroupForm()
    
    context = {
        'workspace': workspace,
        'groups': groups_list,
        'user_membership': user_membership,
        'form': form,
    }
    return render(request, 'team/groups.html', context)


@login_required
@workspace_admin_required
def group_detail(request, workspace_id, group_id):
    """
    Group detail page - view and manage group members
    """
    workspace = get_object_or_404(Workspace, id=workspace_id)
    group = get_object_or_404(Group, id=group_id, workspace=workspace)
    
    # Get all workspace members not in this group
    workspace_members = User.objects.filter(
        memberships__workspace=workspace
    ).exclude(
        group_memberships__group=group
    ).distinct()
    
    if request.method == 'POST':
        if 'add_member' in request.POST:
            member_form = GroupMembershipForm(request.POST, workspace=workspace)
            if member_form.is_valid():
                group_membership = member_form.save(commit=False)
                group_membership.group = group
                group_membership.added_by = request.user
                group_membership.save()
                
                ActivityLog.objects.create(
                    workspace=workspace,
                    user=request.user,
                    action=f"added {group_membership.user.username} to group '{group.name}'"
                )
                
                messages.success(request, f"Added {group_membership.user.username} to group")
                return redirect('team:group-detail', workspace_id=workspace_id, group_id=group_id)
        elif 'update_group' in request.POST:
            group_form = GroupForm(request.POST, instance=group)
            if group_form.is_valid():
                group_form.save()
                
                ActivityLog.objects.create(
                    workspace=workspace,
                    user=request.user,
                    action=f"updated group '{group.name}'"
                )
                
                messages.success(request, f"Group '{group.name}' updated successfully!")
                return redirect('team:group-detail', workspace_id=workspace_id, group_id=group_id)
    else:
        member_form = GroupMembershipForm(workspace=workspace)
        group_form = GroupForm(instance=group)
    
    context = {
        'workspace': workspace,
        'group': group,
        'workspace_members': workspace_members,
        'member_form': member_form,
        'group_form': group_form,
    }
    return render(request, 'team/group_detail.html', context)


@login_required
@workspace_admin_required
def remove_group_member(request, workspace_id, group_id, membership_id):
    """
    Remove a member from a group
    """
    workspace = get_object_or_404(Workspace, id=workspace_id)
    group = get_object_or_404(Group, id=group_id, workspace=workspace)
    group_membership = get_object_or_404(GroupMembership, id=membership_id, group=group)
    
    user_email = group_membership.user.email
    group_membership.delete()
    
    ActivityLog.objects.create(
        workspace=workspace,
        user=request.user,
        action=f"removed {user_email} from group '{group.name}'"
    )
    
    messages.success(request, f"Removed {user_email} from {group.name}")
    return redirect('team:group-detail', workspace_id=workspace_id, group_id=group_id)


@login_required
@workspace_admin_required
def delete_group(request, workspace_id, group_id):
    """
    Delete a group entirely
    """
    workspace = get_object_or_404(Workspace, id=workspace_id)
    group = get_object_or_404(Group, id=group_id, workspace=workspace)
    group_name = group.name
    
    group.delete()
    
    ActivityLog.objects.create(
        workspace=workspace,
        user=request.user,
        action=f"deleted group '{group_name}'"
    )
    
    messages.success(request, f"Group '{group_name}' deleted successfully")
    return redirect('team:groups', workspace_id=workspace_id)