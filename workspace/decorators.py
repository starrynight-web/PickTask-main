from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Membership, Workspace

def workspace_required(view_func):
    def wrapper(request, workspace_id, *args, **kwargs):
        workspace = get_object_or_404(Workspace, id=workspace_id)
        
        # Check if user is member of this workspace
        if not Membership.objects.filter(user=request.user, workspace=workspace).exists():
            messages.error(request, "You don't have access to this workspace")
            return redirect('workspace:dashboard')
        
        return view_func(request, workspace_id, *args, **kwargs)
    return wrapper

def workspace_admin_required(view_func):
    def wrapper(request, workspace_id, *args, **kwargs):
        workspace = get_object_or_404(Workspace, id=workspace_id)
        
        # Check if user is admin of this workspace
        membership = Membership.objects.filter(
            user=request.user, 
            workspace=workspace,
            role='admin'
        ).first()
        
        if not membership:
            messages.error(request, "Admin access required for this action")
            return redirect('workspace:dashboard')
        
        return view_func(request, workspace_id, *args, **kwargs)
    return wrapper