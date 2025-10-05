"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
    from django.urls import path, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from workspace.views import dashboard

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', dashboard, name='home'),
    path('auth/', include('authentication.urls')),
    path('workspace/', include('workspace.urls')),
    path('kanban/', include('kanban.urls')),
    path('team/', include('team.urls')),
    path('task/', include('task.urls')),
    path('activity/', include('activity.urls')),
]
"""
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('auth/', include('authentication.urls')),
    path('workspace/', include('workspace.urls', namespace='workspace')),
    path('kanban/', include('kanban.urls')),
    path('task/', include('task.urls')),
    path('team/', include('team.urls')),
    path('activity/', include('activity.urls')),

]
