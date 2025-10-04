from django.urls import path
from . import views

app_name = 'task'

urlpatterns = [
    path('<int:pk>/', views.TaskDetailView.as_view(), name='task-detail'),
    path('<int:workspace_id>/create/', views.TaskCreateView.as_view(), name='create-task'),
    path('<int:workspace_id>/edit/<int:pk>/', views.TaskUpdateView.as_view(), name='edit-task'),
]