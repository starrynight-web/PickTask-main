from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from workspace.models import Workspace, Project, Task, ActivityLog
from workspace.decorators import workspace_required
from workspace.forms import TaskForm

@login_required
@workspace_required
def kanban_board(request, workspace_id):
 
    workspace = get_object_or_404(Workspace, id=workspace_id)
 
    projects = Project.objects.filter(workspace=workspace)

    project_id = request.GET.get('project')
    if project_id:
        tasks = Task.objects.filter(project__id=project_id, project__workspace=workspace)
        current_project = get_object_or_404(Project, id=project_id, workspace=workspace)
    else:
        tasks = Task.objects.filter(project__workspace=workspace)
        current_project = None
 
    tasks_by_status = {
        'todo': tasks.filter(status='todo').select_related('project', 'assigned_to'),
        'in_progress': tasks.filter(status='in_progress').select_related('project', 'assigned_to'),
        'review': tasks.filter(status='review').select_related('project', 'assigned_to'),
        'done': tasks.filter(status='done').select_related('project', 'assigned_to'),
    }
    
    context = {
        'workspace': workspace,
        'projects': projects,
        'current_project': current_project,
        'tasks_by_status': tasks_by_status,
        'status_choices': Task.STATUS_CHOICES,
        'priority_choices': Task.PRIORITY_CHOICES,
    }
    
    return render(request, 'kanban/kanban.html', context)

@login_required
@workspace_required
def update_task_status(request, workspace_id):
    """
    AJAX view to update task status (drag & drop)
    """
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        task_id = request.POST.get('task_id')
        new_status = request.POST.get('status')
        
        try:
            task = Task.objects.get(
                id=task_id, 
                project__workspace__id=workspace_id
            )
            old_status = task.status
            task.status = new_status
            task.save()
            
            # Log activity
            ActivityLog.objects.create(
                workspace=task.project.workspace,
                user=request.user,
                action=f"moved task '{task.title}' from {old_status} to {new_status}"
            )
            
            return JsonResponse({
                'success': True,
                'task_title': task.title,
                'old_status': old_status,
                'new_status': new_status
            })
            
        except Task.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Task not found'}, status=404)
    
    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)

@login_required
@workspace_required
def quick_create_task(request, workspace_id):
  
    workspace = get_object_or_404(Workspace, id=workspace_id)
    
    if request.method == 'POST':
        title = request.POST.get('title')
        project_id = request.POST.get('project_id')  # Fixed: was 'project'
        status = request.POST.get('status', 'todo')
        
        if title and project_id:
            try:
                project = Project.objects.get(id=project_id, workspace=workspace)
                task = Task.objects.create(
                    title=title,
                    project=project,
                    status=status,
                    created_by=request.user
                )
                
                # Log activity
                ActivityLog.objects.create(
                    workspace=workspace,
                    user=request.user,
                    action=f"created task '{task.title}' in {task.get_status_display()} column"
                )
                
                messages.success(request, f"Task '{task.title}' created successfully!")
                return redirect('kanban:kanban', workspace_id=workspace_id)
                
            except Project.DoesNotExist:
                messages.error(request, "Invalid project selected")
        else:
            messages.error(request, "Please provide both title and project")
    
    return redirect('kanban:kanban', workspace_id=workspace_id)