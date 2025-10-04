from django.apps import AppConfig

class WorkspaceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'workspace'
    verbose_name = 'Workspace Management'
    
    def ready(self):
        # This import will now work because signals.py exists
        import workspace.signals