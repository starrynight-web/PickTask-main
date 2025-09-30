from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('workspaces/', views.workspaces, name="workspaces"),
    path('tasks/', views.tasks, name="tasks"),
]
