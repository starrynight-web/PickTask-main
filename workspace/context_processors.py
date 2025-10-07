from .models import Membership, Workspace


def workspace_context(request):
    context = {}

    if request.user.is_authenticated:
        try:     
            user_memberships = Membership.objects.filter(
                user=request.user
            ).select_related('workspace')
            workspaces = [
                membership.workspace for membership in user_memberships]

            current_workspace = None

            workspace_id = request.resolver_match.kwargs.get(
                'workspace_id') if request.resolver_match else None

            if workspace_id:
                current_workspace = next(
                    (ws for ws in workspaces if ws.id == int(workspace_id)), None)
                # Store in session when we get it from URL
                if current_workspace:
                    request.session['current_workspace_id'] = current_workspace.id

            if not current_workspace:
                session_workspace_id = request.session.get(
                    'current_workspace_id')
                if session_workspace_id:
                    current_workspace = next(
                        (ws for ws in workspaces if ws.id == session_workspace_id), None)

            if not current_workspace and workspaces:
                current_workspace = workspaces[0]
       
                if current_workspace:
                    request.session['current_workspace_id'] = current_workspace.id

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
     
            print(f"Context processor error: {e}")

    return context
