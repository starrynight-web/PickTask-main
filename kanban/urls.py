from django.urls import path
from . import views

app_name = 'kanban'

urlpatterns = [
    # Main kanban board
    path('<int:workspace_id>/', views.kanban_board, name='kanban'),
    
    # AJAX endpoints
    path('<int:workspace_id>/update-status/', views.update_task_status, name='update-task-status'),
    path('<int:workspace_id>/quick-create/', views.quick_create_task, name='quick-create-task'),
    path('<int:workspace_id>/quick-create/', views.quick_create_task, name='quick-create-task'),
]