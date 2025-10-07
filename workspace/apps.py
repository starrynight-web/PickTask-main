from django.apps import AppConfig

class WorkspaceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'workspace'
    verbose_name = 'Workspace Management'
    
    def ready(self):
        import workspace.signals