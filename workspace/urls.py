from django.urls import path
from . import views

app_name = 'workspace'

urlpatterns = [
   
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('list/', views.workspace_list, name='workspace-list'),
    path('create/', views.WorkspaceCreateView.as_view(), name='create-workspace'),
    path('confirm/<int:pk>/', views.confirm_workspace, name='confirm-workspace'),
    path('<int:workspace_id>/', views.workspace_detail, name='workspace-detail'),
    path('<int:workspace_id>/projects/create/', views.create_project, name='create-project'),
    path('<int:workspace_id>/select-project/<int:project_id>/', views.select_project, name='select-project'),
    path('<int:workspace_id>/project/<int:project_id>/dashboard/', views.project_dashboard, name='project-dashboard'),
    path('<int:workspace_id>/delete/', views.delete_workspace, name='delete-workspace'),
    path('<int:workspace_id>/projects/<int:project_id>/delete/', views.delete_project, name='delete-project'),
]
