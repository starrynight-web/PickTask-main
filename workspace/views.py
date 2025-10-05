from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.generic import CreateView, UpdateView, DetailView
from django.urls import reverse_lazy
from django.db.models import Count, Q

from .models import Workspace, Membership, Project, Task, ActivityLog
from .forms import WorkspaceForm, ProjectForm, TaskForm
from .decorators import workspace_required, workspace_admin_required


@login_required
def dashboard(request):
    """
    Main dashboard - shows user's workspaces and overview
    """
    # The context processor now handles current_workspace automatically
    # Just get the additional data needed for dashboard

    current_workspace = getattr(request, 'current_workspace', None)

    context = {}

    if current_workspace:
        # Get workspace statistics
        projects = Project.objects.filter(workspace=current_workspace)
        tasks = Task.objects.filter(project__workspace=current_workspace)

        # Task counts by status
        task_counts = {
            'total': tasks.count(),
            'todo': tasks.filter(status='todo').count(),
            'in_progress': tasks.filter(status='in_progress').count(),
            'review': tasks.filter(status='review').count(),
            'done': tasks.filter(status='done').count(),
        }

        # Recent activities
        recent_activities = ActivityLog.objects.filter(
            workspace=current_workspace
        ).select_related('user').order_by('-timestamp')[:10]

        context.update({
            'projects': projects[:5],  # Show only 5 recent projects
            'total_tasks': task_counts['total'],
            'completed_tasks': task_counts['done'],
            'recent_activities': recent_activities,
        })

    return render(request, 'workspace/dashboard.html', context)


@login_required
def workspace_detail(request, workspace_id):
    """
    Specific workspace overview
    """
    workspace = get_object_or_404(Workspace, id=workspace_id)

    # Check if user has access to this workspace
    if not Membership.objects.filter(user=request.user, workspace=workspace).exists():
        messages.error(request, "You don't have access to this workspace")
        return redirect('workspace:dashboard')

    # The context processor will automatically set this as current workspace
    # because it's in the URL

    # Get workspace statistics
    projects = Project.objects.filter(workspace=workspace)
    tasks = Task.objects.filter(project__workspace=workspace)

    context = {
        'workspace': workspace,
        'projects': projects,
        'total_tasks': tasks.count(),
        'recent_activities': ActivityLog.objects.filter(
            workspace=workspace
        ).select_related('user').order_by('-timestamp')[:10],
    }

    return render(request, 'workspace/workspace.html', context)


class WorkspaceCreateView(CreateView):
    model = Workspace
    form_class = WorkspaceForm
    template_name = 'workspace/create-workspace.html'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        response = super().form_valid(form)

        # Create membership for creator as admin
        Membership.objects.create(
            user=self.request.user,
            workspace=form.instance,
            role='admin'
        )

        # Set the newly created workspace as current in session
        self.request.session['current_workspace_id'] = self.object.id

        # Log activity
        ActivityLog.objects.create(
            workspace=form.instance,
            user=self.request.user,
            action=f"created workspace '{form.instance.name}'"
        )

        messages.success(
            self.request, f"Workspace '{form.instance.name}' created successfully!")
        return response

    def get_success_url(self):
        return reverse_lazy('workspace:confirm-workspace', kwargs={'pk': self.object.pk})


@login_required
def confirm_workspace(request, pk):
    """
    Confirmation page after workspace creation
    """
    workspace = get_object_or_404(Workspace, pk=pk)

    # Verify user has access
    if not Membership.objects.filter(user=request.user, workspace=workspace).exists():
        messages.error(request, "You don't have access to this workspace")
        return redirect('workspace:dashboard')

    # The context processor will handle setting this as current workspace
    # because we're storing it in session during creation

    return render(request, 'workspace/confirm-workspace.html', {'workspace': workspace})


@login_required
def create_project(request, workspace_id):
    """
    Create a new project in a workspace
    """
    workspace = get_object_or_404(Workspace, id=workspace_id)

    # Check if user has access
    if not Membership.objects.filter(user=request.user, workspace=workspace).exists():
        messages.error(request, "You don't have access to this workspace")
        return redirect('workspace:dashboard')

    # The context processor will automatically set this as current workspace
    # because it's in the URL

    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.workspace = workspace
            project.created_by = request.user
            project.save()

            # Log activity
            ActivityLog.objects.create(
                workspace=workspace,
                user=request.user,
                action=f"created project '{project.name}'"
            )

            messages.success(
                request, f"Project '{project.name}' created successfully!")
            return redirect('workspace:workspace-detail', workspace_id=workspace_id)
    else:
        form = ProjectForm()

    context = {
        'workspace': workspace,
        'form': form,
    }
    return render(request, 'workspace/create-project.html', context)


@login_required
def workspace_list(request):
    """
    Simple list of user's workspaces
    """
    memberships = Membership.objects.filter(
        user=request.user).select_related('workspace')

    context = {
        'memberships': memberships,
    }
    return render(request, 'workspace/workspace_list.html', context)
