from django.urls import path
from . import views

app_name = 'activity'

urlpatterns = [
    # Main activity log
    path('<int:workspace_id>/', views.activity_log, name='activity'),
    path('<int:workspace_id>/summary/', views.activity_summary, name='summary'),
    path('<int:workspace_id>/user/<int:user_id>/', views.user_activity, name='user-activity'),
]