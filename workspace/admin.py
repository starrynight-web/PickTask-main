from django.contrib import admin
from .models import Workspace, Membership, Project, Task, ActivityLog

@admin.register(Workspace)
class WorkspaceAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_by', 'created_at', 'member_count']
    list_filter = ['created_at']
    search_fields = ['name', 'created_by__username']
    readonly_fields = ['created_at']
    
    def member_count(self, obj):
        return obj.memberships.count()
    member_count.short_description = 'Members'

@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ['user', 'workspace', 'role', 'joined_at']
    list_filter = ['role', 'joined_at', 'workspace']
    search_fields = ['user__username', 'workspace__name']
    readonly_fields = ['joined_at']

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'workspace', 'created_by', 'created_at', 'task_count']
    list_filter = ['workspace', 'created_at']
    search_fields = ['name', 'workspace__name']
    readonly_fields = ['created_at']
    
    def task_count(self, obj):
        return obj.tasks.count()
    task_count.short_description = 'Tasks'

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'project', 'status', 'priority', 'assigned_to', 'due_date', 'created_at']
    list_filter = ['status', 'priority', 'due_date', 'created_at']
    search_fields = ['title', 'description', 'project__name']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'

@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'workspace', 'action_short', 'timestamp']
    list_filter = ['timestamp', 'workspace']
    search_fields = ['user__username', 'action', 'workspace__name']
    readonly_fields = ['timestamp']
    
    def action_short(self, obj):
        return obj.action[:50] + '...' if len(obj.action) > 50 else obj.action
    action_short.short_description = 'Action'