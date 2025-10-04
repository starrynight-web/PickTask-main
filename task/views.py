from django.views.generic import CreateView, UpdateView, DetailView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404

from workspace.models import Task, Project, Workspace
from workspace.forms import TaskForm
from workspace.decorators import workspace_required

@method_decorator([login_required, workspace_required], name='dispatch')
class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'task/create_task.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        workspace_id = self.kwargs.get('workspace_id')
        if workspace_id:
            workspace = get_object_or_404(Workspace, id=workspace_id)
            kwargs['workspace'] = workspace
        return kwargs

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('task:task-detail', kwargs={'pk': self.object.pk})

@method_decorator([login_required, workspace_required], name='dispatch')
class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'task/create_task.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        workspace = self.object.project.workspace
        kwargs['workspace'] = workspace
        return kwargs

    def get_success_url(self):
        return reverse_lazy('task:task-detail', kwargs={'pk': self.object.pk})

@method_decorator(login_required, name='dispatch')
class TaskDetailView(DetailView):
    model = Task
    template_name = 'task/task_detail.html'
    context_object_name = 'task'

    def get_queryset(self):
        return Task.objects.filter(project__workspace__memberships__user=self.request.user)