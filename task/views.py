from django.views.generic import CreateView, UpdateView, DetailView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

from workspace.models import Task, Project, Workspace
from workspace.forms import TaskForm, CommentForm
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        workspace_id = self.kwargs.get('workspace_id')
        if workspace_id:
            context['workspace'] = get_object_or_404(
                Workspace, id=workspace_id)
        return context

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        workspace_id = self.kwargs.get('workspace_id')
        if workspace_id:
            form.instance.workspace = get_object_or_404(
                Workspace, id=workspace_id)
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['workspace'] = self.object.project.workspace
        return context

    def get_success_url(self):
        return reverse_lazy('task:task-detail', kwargs={'pk': self.object.pk})


@method_decorator(login_required, name='dispatch')
class TaskDetailView(DetailView):
    model = Task
    template_name = 'task/task_detail.html'
    context_object_name = 'task'

    def get_queryset(self):
        return Task.objects.filter(project__workspace__memberships__user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task = self.get_object()
        context['workspace'] = task.project.workspace
        context['comment_form'] = CommentForm()
        context['comments'] = task.comments.select_related('author').all()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.task = self.object
            comment.author = request.user
            comment.save()

            # Log activity
            from workspace.models import ActivityLog
            ActivityLog.objects.create(
                workspace=self.object.project.workspace,
                user=request.user,
                action=f"commented on task '{self.object.title}'"
            )

            messages.success(request, "Comment added successfully!")
        else:
            messages.error(request, "Failed to add comment.")

        return self.get(request, *args, **kwargs)  # ← Redirect to same page