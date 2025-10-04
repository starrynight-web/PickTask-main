from django.urls import path
from . import views

app_name = 'team'

urlpatterns = [
    # Team management
    path('<int:workspace_id>/', views.team_management, name='team'),
    path('<int:workspace_id>/invite/', views.invite_member, name='invite'),
    path('<int:workspace_id>/roles/<int:membership_id>/', views.edit_role, name='edit-role'),
    path('<int:workspace_id>/remove/<int:membership_id>/', views.remove_member, name='remove-member'),
    
  
    path('<int:workspace_id>/groups/', views.groups, name='groups'),
    path('<int:workspace_id>/groups/<int:group_id>/', views.group_detail, name='group-detail'),
    path('<int:workspace_id>/groups/<int:group_id>/remove-member/<int:membership_id>/', views.remove_group_member, name='remove-group-member'),
    path('<int:workspace_id>/groups/<int:group_id>/delete/', views.delete_group, name='delete-group'),
]