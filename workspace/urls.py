from django.urls import path
from . import views

app_name = 'workspace'

urlpatterns = [
    # Dashboard and workspace management
    path('', views.dashboard, name='dashboard'),
    path('list/', views.workspace_list, name='workspace-list'),
    path('create/', views.WorkspaceCreateView.as_view(), name='create-workspace'),
    path('confirm/<int:pk>/', views.confirm_workspace, name='confirm-workspace'),
    path('<int:workspace_id>/', views.workspace_detail, name='workspace-detail'), 
    path('<int:workspace_id>/projects/create/', views.create_project, name='create-project'),



]

