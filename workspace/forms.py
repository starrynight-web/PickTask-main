from django import forms
from .models import Workspace, Project, Task, Membership
from django.contrib.auth import get_user_model

User = get_user_model()

class WorkspaceForm(forms.ModelForm):
    class Meta:
        model = Workspace
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter workspace name',
                'autofocus': True
            }),
        }
        labels = {
            'name': 'Workspace Name'
        }

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'color']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Project name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-textarea', 
                'rows': 3,
                'placeholder': 'Project description (optional)'
            }),
            'color': forms.TextInput(attrs={
                'type': 'color', 
                'class': 'form-color h-10 w-15'
            }),
        }

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'project', 'assigned_to', 'status', 'priority', 'due_date']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Task title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-textarea', 
                'rows': 4,
                'placeholder': 'Task description (optional)'
            }),
            'project': forms.Select(attrs={'class': 'form-select'}),
            'assigned_to': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
            'due_date': forms.DateTimeInput(attrs={
                'type': 'datetime-local', 
                'class': 'form-input'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        workspace = kwargs.pop('workspace', None)
        super().__init__(*args, **kwargs)
        
        if workspace:
            self.fields['project'].queryset = Project.objects.filter(workspace=workspace)
            self.fields['assigned_to'].queryset = User.objects.filter(
                memberships__workspace=workspace
            ).distinct()

class InviteForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'Enter email address'
        })
    )
    role = forms.ChoiceField(
        choices=Membership.ROLE_CHOICES,
        initial='member',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

class RoleAssignmentForm(forms.ModelForm):
    class Meta:
        model = Membership
        fields = ['role']
        widgets = {
            'role': forms.Select(attrs={'class': 'form-select'}),
        }