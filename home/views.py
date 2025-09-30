from django.shortcuts import render
from .models import Workspace, Task
# Create your views here.


def home(request):
    return render(request, "home/index.html")
def feature(request):
    return render(request, "home/feature.html")
def about_us(request):
    return render(request, 'home/about_us.html')

def blog(request):
    return render(request, 'home/blog.html')

def contact(request):
    return render(request, 'home/contact.html')

def documentation(request):
    return render(request, 'home/documentation.html')

def help_support(request):
    return render(request, 'home/help_support.html')

def integrations(request):
    return render(request, 'home/integrations.html')

def pricing(request):
    return render(request, 'home/pricing.html')

def tutorial(request):
    return render(request, 'home/tutorial.html')
def workspaces(request):
    data = Workspace.objects.all()
    return render(request, "home/workspaces.html", {"workspaces": data})

def tasks(request):
    data = Task.objects.all()
    return render(request, "home/tasks.html", {"tasks": data})
