from .models import Membership, Workspace, Project


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
            current_project = None

            # Get workspace from URL or session
            workspace_id = request.resolver_match.kwargs.get(
                'workspace_id') if request.resolver_match else None

            if workspace_id:
                current_workspace = next(
                    (ws for ws in workspaces if ws.id == int(workspace_id)), None)
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

            # PROJECT HANDLING
            if current_workspace:
                # Get project from URL
                project_id = request.resolver_match.kwargs.get(
                    'project_id') if request.resolver_match else None

                if project_id:
                    try:
                        current_project = Project.objects.get(
                            id=project_id,
                            workspace=current_workspace
                        )
                        request.session['current_project_id'] = current_project.id
                    except Project.DoesNotExist:
                        if 'current_project_id' in request.session:
                            del request.session['current_project_id']

                # If no project from URL, try session
                if not current_project:
                    session_project_id = request.session.get(
                        'current_project_id')
                    if session_project_id:
                        try:
                            current_project = Project.objects.get(
                                id=session_project_id,
                                workspace=current_workspace
                            )
                        except Project.DoesNotExist:
                            if 'current_project_id' in request.session:
                                del request.session['current_project_id']

                # Auto-select first project if none selected
                if not current_project and current_workspace.projects.exists():
                    current_project = current_workspace.projects.first()
                    if current_project:
                        request.session['current_project_id'] = current_project.id

            user_membership = None
            if current_workspace:
                user_membership = Membership.objects.filter(
                    user=request.user,
                    workspace=current_workspace
                ).first()

            context.update({
                'workspaces': workspaces,
                'current_workspace': current_workspace,
                'current_project': current_project,
                'user_membership': user_membership,
            })

        except Exception as e:
            print(f"Context processor error: {e}")

    return context
