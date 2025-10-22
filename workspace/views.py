from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.generic import CreateView, UpdateView, DetailView
from django.urls import reverse_lazy
from django.db.models import Count, Q
from django.core.exceptions import PermissionDenied

from .models import Workspace, Membership, Project, Task, ActivityLog
from .forms import WorkspaceForm, ProjectForm, TaskForm
from .decorators import workspace_required, workspace_admin_required


# ✅ NEW: Neutral home page after login
@login_required
def home(request):
    """Neutral landing page — no auto-selection."""
    memberships = Membership.objects.filter(
        user=request.user
    ).select_related('workspace')
    
    context = {
        'memberships': memberships,
    }
    return render(request, 'workspace/home.html', context)


@login_required
def dashboard(request):
    # Read from session (set by workspace_detail or select_project)
    workspace_id = request.session.get('current_workspace_id')
    project_id = request.session.get('current_project_id')

    current_workspace = None
    current_project = None
    projects = []
    total_tasks = 0
    completed_tasks = 0
    recent_activities = []
    project_specific = False

    if workspace_id:
        try:
            current_workspace = Workspace.objects.get(id=workspace_id)
            # Verify membership
            if not current_workspace.memberships.filter(user=request.user).exists():
                messages.error(request, "You don't have access to this workspace.")
                del request.session['current_workspace_id']
                if 'current_project_id' in request.session:
                    del request.session['current_project_id']
                return redirect('workspace:home')

            # Get projects
            projects = current_workspace.projects.all()[:5]

            # Handle project context
            if project_id:
                try:
                    current_project = Project.objects.get(id=project_id, workspace=current_workspace)
                    # Count tasks for this project
                    tasks = Task.objects.filter(project=current_project)
                    project_specific = True
                except Project.DoesNotExist:
                    current_project = None
                    project_id = None
                    if 'current_project_id' in request.session:
                        del request.session['current_project_id']
                    tasks = Task.objects.filter(project__workspace=current_workspace)
            else:
                tasks = Task.objects.filter(project__workspace=current_workspace)

            total_tasks = tasks.count()
            completed_tasks = tasks.filter(status='done').count()

            # ✅ Fresh activity log
            recent_activities = ActivityLog.objects.filter(
                workspace=current_workspace
            ).select_related('user').order_by('-timestamp')[:10]

        except Workspace.DoesNotExist:
            current_workspace = None
            if 'current_workspace_id' in request.session:
                del request.session['current_workspace_id']

    context = {
        'current_workspace': current_workspace,
        'current_project': current_project,
        'projects': projects,
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'recent_activities': recent_activities,
        'project_specific': project_specific,
    }

    return render(request, 'workspace/dashboard.html', context)


@login_required
def workspace_detail(request, workspace_id):
    workspace = get_object_or_404(Workspace, id=workspace_id)

    # Verify access
    if not Membership.objects.filter(user=request.user, workspace=workspace).exists():
        messages.error(request, "You don't have access to this workspace")
        return redirect('workspace:home')

    # Store workspace in session
    request.session['current_workspace_id'] = workspace_id
    # Reset project when workspace changes
    request.session['current_project_id'] = None

    # Check if workspace has projects
    projects = workspace.projects.all()

    # If there are projects, auto-select the first one and redirect to dashboard
    if projects.exists():
        # Auto-select first project
        first_project = projects.first()
        request.session['current_project_id'] = first_project.id

        messages.success(
            request, f"Selected workspace: {workspace.name} and project: {first_project.name}")
        return redirect('workspace:dashboard')
    else:
        # No projects - redirect to create project
        messages.info(request, "Create your first project for this workspace")
        return redirect('workspace:create-project', workspace_id=workspace_id)


class WorkspaceCreateView(CreateView):
    model = Workspace
    form_class = WorkspaceForm
    template_name = 'workspace/create-workspace.html'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        response = super().form_valid(form)

        Membership.objects.create(
            user=self.request.user,
            workspace=form.instance,
            role='admin'
        )

        self.request.session['current_workspace_id'] = self.object.id

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
    workspace = get_object_or_404(Workspace, pk=pk)

    if not Membership.objects.filter(user=request.user, workspace=workspace).exists():
        messages.error(request, "You don't have access to this workspace")
        return redirect('workspace:home')

    return render(request, 'workspace/confirm-workspace.html', {'workspace': workspace})


@login_required
def create_project(request, workspace_id):
    workspace = get_object_or_404(Workspace, id=workspace_id)

    if not Membership.objects.filter(user=request.user, workspace=workspace).exists():
        messages.error(request, "You don't have access to this workspace")
        return redirect('workspace:home')

    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.workspace = workspace
            project.created_by = request.user
            project.save()

            ActivityLog.objects.create(
                workspace=workspace,
                user=request.user,
                action=f"created project '{project.name}'"
            )

            messages.success(
                request, f"Project '{project.name}' created successfully!")
            return redirect('workspace:workspace-detail', workspace_id=workspace_id)
        else:
            context = {
                'workspace': workspace,
                'form': form,
            }
            return render(request, 'workspace/create-project.html', context)
    else:
        form = ProjectForm()

    context = {
        'workspace': workspace,
        'form': form,
    }
    return render(request, 'workspace/create-project.html', context)


@login_required
def workspace_list(request):
    memberships = Membership.objects.filter(
        user=request.user
    ).select_related('workspace')

    context = {
        'memberships': memberships,
    }
    return render(request, 'workspace/workspace_list.html', context)


@login_required
def select_project(request, workspace_id, project_id):
    """Handle project selection"""
    workspace = get_object_or_404(Workspace, id=workspace_id)
    project = get_object_or_404(Project, id=project_id, workspace=workspace)

    # Verify user access
    if not Membership.objects.filter(user=request.user, workspace=workspace).exists():
        messages.error(request, "You don't have access to this workspace")
        return redirect('workspace:home')

    # Store selections in session
    request.session['current_workspace_id'] = workspace_id
    request.session['current_project_id'] = project_id

    messages.success(request, f"Selected project: {project.name}")
    return redirect('workspace:dashboard')


@login_required
def project_dashboard(request, workspace_id, project_id):
    """Project-specific dashboard"""
    request.session['current_workspace_id'] = workspace_id
    request.session['current_project_id'] = project_id
    return redirect('workspace:dashboard')


# ✅ NEW: Delete Workspace (Admin Only)
@login_required
@workspace_admin_required
def delete_workspace(request, workspace_id):
    workspace = get_object_or_404(Workspace, id=workspace_id)
    
    if request.method == 'POST':
        workspace_name = workspace.name
        workspace.delete()
        messages.success(request, f'Workspace "{workspace_name}" has been deleted.')
        return redirect('workspace:home')
    
    return render(request, 'workspace/confirm_delete.html', {
        'item_type': 'workspace',
        'item_name': workspace.name,
    })


# ✅ NEW: Delete Project (Admin or Creator)
@login_required
def delete_project(request, workspace_id, project_id):
    workspace = get_object_or_404(Workspace, id=workspace_id)
    project = get_object_or_404(Project, id=project_id, workspace=workspace)
    
    # Only admins or project creator can delete
    if not (request.user == project.created_by or 
            workspace.memberships.filter(user=request.user, role='admin').exists()):
        messages.error(request, "You don't have permission to delete this project.")
        return redirect('workspace:dashboard')
    
    if request.method == 'POST':
        project_name = project.name
        project.delete()
        messages.success(request, f'Project "{project_name}" has been deleted.')
        return redirect('workspace:workspace-detail', workspace_id=workspace_id)
    
    return render(request, 'workspace/confirm_delete.html', {
        'item_type': 'project',
        'item_name': project.name,
    })