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
    current_workspace = getattr(request, 'current_workspace', None)
    current_project = getattr(request, 'current_project', None)

    context = {}

    if current_workspace:
        # Get workspace projects
        projects = Project.objects.filter(workspace=current_workspace)

        # If we have a current project, filter tasks by project
        if current_project:
            tasks = Task.objects.filter(project=current_project)
            project_specific = True
        else:
            # No project selected, show all workspace tasks
            tasks = Task.objects.filter(project__workspace=current_workspace)
            project_specific = False

        task_counts = {
            'total': tasks.count(),
            'todo': tasks.filter(status='todo').count(),
            'in_progress': tasks.filter(status='in_progress').count(),
            'review': tasks.filter(status='review').count(),
            'done': tasks.filter(status='done').count(),
        }

        recent_activities = ActivityLog.objects.filter(
            workspace=current_workspace
        ).select_related('user').order_by('-timestamp')[:10]

        context.update({
            'projects': projects[:5],
            'total_tasks': task_counts['total'],
            'completed_tasks': task_counts['done'],
            'recent_activities': recent_activities,
            'project_specific': project_specific,
        })

    return render(request, 'workspace/dashboard.html', context)


@login_required
def workspace_detail(request, workspace_id):
    workspace = get_object_or_404(Workspace, id=workspace_id)

    # Verify access
    if not Membership.objects.filter(user=request.user, workspace=workspace).exists():
        messages.error(request, "You don't have access to this workspace")
        return redirect('workspace:dashboard')

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
        return redirect('workspace:dashboard')

    return render(request, 'workspace/confirm-workspace.html', {'workspace': workspace})


@login_required
def create_project(request, workspace_id):
    workspace = get_object_or_404(Workspace, id=workspace_id)

    if not Membership.objects.filter(user=request.user, workspace=workspace).exists():
        messages.error(request, "You don't have access to this workspace")
        return redirect('workspace:dashboard')

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
            # ✅ CRITICAL: Re-render with invalid form to show errors
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
        return redirect('workspace:dashboard')

    # Store selections in session
    request.session['current_workspace_id'] = workspace_id
    request.session['current_project_id'] = project_id

    messages.success(request, f"Selected project: {project.name}")
    return redirect('workspace:dashboard')


@login_required
def project_dashboard(request, workspace_id, project_id):
    """Project-specific dashboard"""
    # Store in session and redirect to main dashboard
    request.session['current_workspace_id'] = workspace_id
    request.session['current_project_id'] = project_id
    return redirect('workspace:dashboard')
