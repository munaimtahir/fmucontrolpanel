from django.contrib import admin
from .models import Project, Task, Link, LogEntry


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'status', 'risk', 'updated_at']
    list_filter = ['status', 'risk']
    search_fields = ['name', 'description']


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'project', 'status', 'priority', 'due_date']
    list_filter = ['status', 'priority', 'project']
    search_fields = ['title', 'description']


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ['title', 'project', 'link_type', 'url']
    list_filter = ['link_type', 'project']
    search_fields = ['title', 'url']


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ['project', 'message', 'timestamp']
    list_filter = ['project', 'timestamp']
    search_fields = ['message']
