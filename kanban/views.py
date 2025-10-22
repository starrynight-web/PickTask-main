from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from django.db import transaction
from django.views.decorators.http import require_POST
from django.db.models import Max
import json

from workspace.models import Workspace, Project, Task, StatusColumn, ActivityLog
from workspace.decorators import workspace_required


def ensure_default_status_columns(workspace):
    
    if not workspace.status_columns.exists():
        default_names = ['To Do', 'In Progress', 'Review', 'Done']
        for order, name in enumerate(default_names):
            StatusColumn.objects.create(workspace=workspace, name=name, order=order)


@login_required
@workspace_required
def kanban_board(request, workspace_id):
    workspace = get_object_or_404(Workspace, id=workspace_id)
    
 
    ensure_default_status_columns(workspace)
    
    projects = Project.objects.filter(workspace=workspace)

    project_id = request.GET.get('project')
    if project_id:
        tasks = Task.objects.filter(
            project__id=project_id,
            project__workspace=workspace
        ).select_related('project', 'assigned_to', 'status_column')
        current_project = get_object_or_404(Project, id=project_id, workspace=workspace)
    else:
        tasks = Task.objects.filter(
            project__workspace=workspace
        ).select_related('project', 'assigned_to', 'status_column')
        current_project = None

    
    from collections import defaultdict
    tasks_by_column = defaultdict(list)
    for task in tasks:
        col_id = task.status_column.id if task.status_column else None
        tasks_by_column[col_id].append(task)

    status_columns = workspace.status_columns.all()

    context = {
        'workspace': workspace,
        'projects': projects,
        'current_project': current_project,
        'status_columns': status_columns,
        'tasks_by_column': dict(tasks_by_column),
        'has_projects': projects.exists(),
        'empty_list': [],  # For safe template access
    }
    
    return render(request, 'kanban/kanban.html', context)


@login_required
@workspace_required
def update_task_status(request, workspace_id):
    
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            data = json.loads(request.body)
            task_id = data.get('task_id')
            status_column_id = data.get('status_column_id')
        except (json.JSONDecodeError, TypeError):
           
            task_id = request.POST.get('task_id')
            status_column_id = request.POST.get('status_column_id')
        
        try:
            task = Task.objects.select_related('project__workspace', 'status_column').get(
                id=task_id,
                project__workspace__id=workspace_id
            )
            
            old_column = task.status_column
            new_column = get_object_or_404(StatusColumn, id=status_column_id, workspace_id=workspace_id)
            
            task.status_column = new_column
            task.save(update_fields=['status_column'])
            
            # Log activity
            ActivityLog.objects.create(
                workspace=task.project.workspace,
                user=request.user,
                action=f"moved task '{task.title}' to '{new_column.name}'"
            )
            
            return JsonResponse({
                'success': True,
                'task_title': task.title,
                'old_column': old_column.name if old_column else 'None',
                'new_column': new_column.name
            })
            
        except Task.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Task not found'}, status=404)
        except StatusColumn.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Invalid status column'}, status=400)
    
    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)


@login_required
@workspace_required
def quick_create_task(request, workspace_id):
    workspace = get_object_or_404(Workspace, id=workspace_id)
    
    if request.method == 'POST':
        title = request.POST.get('title')
        project_id = request.POST.get('project_id')
        status_column_id = request.POST.get('status_column_id')
        
        if not (title and project_id and status_column_id):
            messages.error(request, "Title, project, and status column are required.")
            return redirect('kanban:kanban', workspace_id=workspace_id)
        
        try:
            project = Project.objects.get(id=project_id, workspace=workspace)
            status_column = StatusColumn.objects.get(id=status_column_id, workspace=workspace)
            
            with transaction.atomic():
                task = Task.objects.create(
                    title=title,
                    project=project,
                    status_column=status_column,
                    created_by=request.user,
                    status='todo'  # keep legacy field as fallback
                )
                
                ActivityLog.objects.create(
                    workspace=workspace,
                    user=request.user,
                    action=f"created task '{task.title}' in '{status_column.name}' column"
                )
            
            messages.success(request, f"Task '{task.title}' created successfully!")
            return redirect('kanban:kanban', workspace_id=workspace_id)
            
        except (Project.DoesNotExist, StatusColumn.DoesNotExist):
            messages.error(request, "Invalid project or status column selected.")
    
    return redirect('kanban:kanban', workspace_id=workspace_id)


@login_required
@workspace_required
@require_POST
def manage_columns(request, workspace_id):
    
    workspace = get_object_or_404(Workspace, id=workspace_id)
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid JSON'})

    action = data.get('action')

    try:
        if action == 'add':
            name = data.get('name', '').strip()
            if not name:
                return JsonResponse({'success': False, 'error': 'Name is required'})
            
            
            if workspace.status_columns.filter(name__iexact=name).exists():
                return JsonResponse({'success': False, 'error': 'A column with this name already exists'})

            
            max_order = workspace.status_columns.aggregate(
                Max('order')
            )['order__max'] or 0
            StatusColumn.objects.create(
                workspace=workspace,
                name=name,
                order=max_order + 1
            )
            return JsonResponse({'success': True})

        elif action == 'rename':
            column_id = data.get('column_id')
            name = data.get('name', '').strip()
            if not name or not column_id:
                return JsonResponse({'success': False, 'error': 'Column ID and name are required'})
            
            column = get_object_or_404(StatusColumn, id=column_id, workspace=workspace)
            if workspace.status_columns.filter(name__iexact=name).exclude(id=column.id).exists():
                return JsonResponse({'success': False, 'error': 'A column with this name already exists'})

            column.name = name
            column.save(update_fields=['name'])
            return JsonResponse({'success': True})

        elif action == 'delete':
            column_id = data.get('column_id')
            if not column_id:
                return JsonResponse({'success': False, 'error': 'Column ID is required'})

            column = get_object_or_404(StatusColumn, id=column_id, workspace=workspace)
            
            
            fallback = workspace.status_columns.exclude(id=column_id).order_by('order').first()
            if not fallback:
                return JsonResponse({'success': False, 'error': 'Cannot delete the last column'})

            with transaction.atomic():
                
                Task.objects.filter(status_column=column).update(status_column=fallback)
                
                column.delete()

            return JsonResponse({'success': True})

        else:
            return JsonResponse({'success': False, 'error': 'Invalid action'})

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})