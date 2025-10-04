from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q

from workspace.models import Workspace, ActivityLog
from workspace.decorators import workspace_required

@login_required
@workspace_required
def activity_log(request, workspace_id):
    """
    Main activity log view with filtering and pagination
    """
    workspace = get_object_or_404(Workspace, id=workspace_id)
    
    # Get all activities for this workspace
    activities = ActivityLog.objects.filter(workspace=workspace).select_related('user').order_by('-timestamp')
    
    # Apply filters from GET parameters
    filter_user = request.GET.get('user')
    filter_action = request.GET.get('action')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    
    if filter_user:
        activities = activities.filter(user__username__icontains=filter_user)
    
    if filter_action:
        activities = activities.filter(action__icontains=filter_action)
    
    if date_from:
        activities = activities.filter(timestamp__date__gte=date_from)
    
    if date_to:
        activities = activities.filter(timestamp__date__lte=date_to)
    
    # Get unique users for filter dropdown
    workspace_users = activities.values_list('user__username', 'user__id').distinct()
    
    # Pagination
    paginator = Paginator(activities, 25)  # 25 activities per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'workspace': workspace,
        'page_obj': page_obj,
        'activities': page_obj.object_list,
        'workspace_users': workspace_users,
        'filter_user': filter_user,
        'filter_action': filter_action,
        'date_from': date_from,
        'date_to': date_to,
        'total_activities': activities.count(),
    }
    
    return render(request, 'activity/activity.html', context)

@login_required
@workspace_required
def activity_summary(request, workspace_id):
    """
    Activity summary with statistics and insights
    """
    workspace = get_object_or_404(Workspace, id=workspace_id)
    
    # Get recent activities (last 30 days)
    from django.utils import timezone
    from datetime import timedelta
    
    thirty_days_ago = timezone.now() - timedelta(days=30)
    recent_activities = ActivityLog.objects.filter(
        workspace=workspace, 
        timestamp__gte=thirty_days_ago
    )
    
    # Calculate statistics
    total_activities = recent_activities.count()
    
    # Most active users
    from django.db.models import Count
    active_users = recent_activities.values('user__username').annotate(
        activity_count=Count('id')
    ).order_by('-activity_count')[:5]
    
    # Common activity types
    common_actions = recent_activities.values('action').annotate(
        count=Count('id')
    ).order_by('-count')[:10]
    
    # Daily activity trend (last 7 days)
    from django.db.models.functions import TruncDate
    daily_activity = recent_activities.filter(
        timestamp__gte=timezone.now() - timedelta(days=7)
    ).annotate(
        date=TruncDate('timestamp')
    ).values('date').annotate(
        count=Count('id')
    ).order_by('date')
    
    context = {
        'workspace': workspace,
        'total_activities': total_activities,
        'active_users': active_users,
        'common_actions': common_actions,
        'daily_activity': list(daily_activity),
        'time_period': '30 days',
    }
    
    return render(request, 'activity/summary.html', context)

@login_required
@workspace_required
def user_activity(request, workspace_id, user_id):
    """
    Activity log for a specific user in the workspace
    """
    workspace = get_object_or_404(Workspace, id=workspace_id)
    
    # Verify the user is a member of this workspace
    from workspace.models import Membership
    user_membership = get_object_or_404(Membership, workspace=workspace, user_id=user_id)
    
    # Get activities for this specific user
    user_activities = ActivityLog.objects.filter(
        workspace=workspace,
        user_id=user_id
    ).select_related('user').order_by('-timestamp')
    
    # Pagination
    paginator = Paginator(user_activities, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'workspace': workspace,
        'page_obj': page_obj,
        'activities': page_obj.object_list,
        'target_user': user_membership.user,
        'total_activities': user_activities.count(),
    }
    
    return render(request, 'activity/user_activity.html', context)