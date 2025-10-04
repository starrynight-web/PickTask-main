from django import forms
from django.contrib.auth import get_user_model

from workspace.models import (
    Workspace, Membership,
    Group, GroupMembership
)

User = get_user_model()


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


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'description', 'color']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Group name (e.g., Developers, Designers)'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-textarea', 
                'rows': 3,
                'placeholder': 'Group description (optional)'
            }),
            'color': forms.TextInput(attrs={
                'type': 'color', 
                'class': 'form-color h-10 w-10'  # Fixed width typo: was 'w-15'
            }),
        }


class GroupMembershipForm(forms.ModelForm):
    class Meta:
        model = GroupMembership
        fields = ['user']
        widgets = {
            'user': forms.Select(attrs={'class': 'form-select'}),
        }
    
    def __init__(self, *args, **kwargs):
        workspace = kwargs.pop('workspace', None)
        super().__init__(*args, **kwargs)
        if workspace:
            self.fields['user'].queryset = User.objects.filter(
                memberships__workspace=workspace
            ).distinct()
        else:
            self.fields['user'].queryset = User.objects.none()