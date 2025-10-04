from .models import Membership, Workspace

def workspace_context(request):
    context = {}
    
    if request.user.is_authenticated:
        try:
            # Get user's memberships with related workspaces
            user_memberships = Membership.objects.filter(
                user=request.user
            ).select_related('workspace')
            workspaces = [membership.workspace for membership in user_memberships]
            
            # Get current workspace from URL or session
            current_workspace = None
            workspace_id = request.resolver_match.kwargs.get('workspace_id') if request.resolver_match else None
            
            if workspace_id:
                current_workspace = next((ws for ws in workspaces if ws.id == int(workspace_id)), None)
            
            # If no workspace from URL, use first one
            if not current_workspace and workspaces:
                current_workspace = workspaces[0]
            
            # Get user's role in current workspace
            user_membership = None
            if current_workspace:
                user_membership = Membership.objects.filter(
                    user=request.user, 
                    workspace=current_workspace
                ).first()
            
            context.update({
                'workspaces': workspaces,
                'current_workspace': current_workspace,
                'user_membership': user_membership,
            })
            
        except Exception as e:
            # Handle any errors gracefully
            print(f"Context processor error: {e}")
    
    return context