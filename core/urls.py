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
