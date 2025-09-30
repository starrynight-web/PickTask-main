from django.shortcuts import render
from .models import Workspace, Task
# Create your views here.


def home(request):
    return render(request, "home/index.html")

def workspaces(request):
    data = Workspace.objects.all()
    return render(request, "home/workspaces.html", {"workspaces": data})

def tasks(request):
    data = Task.objects.all()
    return render(request, "home/tasks.html", {"tasks": data})
