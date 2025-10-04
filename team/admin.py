from django.contrib import admin
from workspace.models import Group, GroupMembership  # ← Import from workspace, not .models

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'workspace', 'created_by', 'member_count', 'created_at']
    list_filter = ['workspace', 'created_at']
    search_fields = ['name', 'workspace__name']
    
    def member_count(self, obj):
        return obj.member_count()
    member_count.short_description = 'Members'

@admin.register(GroupMembership)
class GroupMembershipAdmin(admin.ModelAdmin):
    list_display = ['user', 'group', 'added_by', 'added_at']
    list_filter = ['added_at', 'group__workspace']
    search_fields = ['user__username', 'group__name']