from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.



# User (custom)
class User(AbstractUser):
    full_name = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


# Workspace
class Workspace(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class UserWorkspace(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE)
    role = models.CharField(max_length=50)

    class Meta:
        unique_together = ("user", "workspace")


# Spaces / Lists
class Space(models.Model):
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)


class Folder(models.Model):
    space = models.ForeignKey(Space, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)


class List(models.Model):
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, null=True, blank=True)
    space = models.ForeignKey(Space, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)


# Tasks / Subtasks
class Task(models.Model):
    list = models.ForeignKey(List, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=50)
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Subtask(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=50)
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


#  Comments, Attachments, Logs
class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Attachment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    file_path = models.TextField()
    uploaded_at = models.DateTimeField(auto_now_add=True)


class ActivityLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)


#  Custom fields
class CustomField(models.Model):
    name = models.CharField(max_length=255)
    field_type = models.CharField(max_length=50)


class TaskCustomField(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    custom_field = models.ForeignKey(CustomField, on_delete=models.CASCADE)
    value = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ("task", "custom_field")


#  Tags
class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True)


class TaskTag(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("task", "tag")


#  Time logs
class TimeLog(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
