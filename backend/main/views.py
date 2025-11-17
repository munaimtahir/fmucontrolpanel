from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.utils import timezone
from .models import Project, Task, Link, LogEntry
from .github_client import GitHubClient


def home(request):
    """Dashboard view listing all projects"""
    projects = Project.objects.all()
    return render(request, 'dashboard.html', {'projects': projects})


def project_detail(request, project_id):
    """Project detail view with editable fields, tasks, links, and logs"""
    project = get_object_or_404(Project, id=project_id)
    
    # Handle project update
    if request.method == 'POST' and request.POST.get('action') == 'update_project':
        project.status = request.POST.get('status', project.status)
        project.risk = request.POST.get('risk', project.risk)
        project.summary = request.POST.get('summary', project.summary)
        project.next_task = request.POST.get('next_task', project.next_task)
        project.save()
        return redirect('project_detail', project_id=project.id)
    
    # Handle new link
    if request.method == 'POST' and request.POST.get('action') == 'add_link':
        Link.objects.create(
            project=project,
            title=request.POST.get('title'),
            url=request.POST.get('url'),
            link_type=request.POST.get('link_type', 'OTHER')
        )
        return redirect('project_detail', project_id=project.id)
    
    # Handle new log entry
    if request.method == 'POST' and request.POST.get('action') == 'add_log':
        LogEntry.objects.create(
            project=project,
            message=request.POST.get('message')
        )
        return redirect('project_detail', project_id=project.id)
    
    tasks = project.tasks.all()
    links = project.links.all()
    logs = project.logs.all()[:10]  # Last 10 log entries
    
    # Fetch GitHub data if repo_name is set
    github_data = {}
    if project.repo_name:
        github = GitHubClient()
        github_data = {
            'pull_requests': github.fetch_pull_requests(project.repo_name),
            'commits': github.fetch_commits(project.repo_name, limit=5),
            'issues': github.fetch_issues(project.repo_name),
        }
    
    return render(request, 'project_detail.html', {
        'project': project,
        'tasks': tasks,
        'links': links,
        'logs': logs,
        'github_data': github_data,
    })


def toggle_task_status(request, task_id):
    """HTMX endpoint to toggle task status"""
    if request.method == 'POST':
        task = get_object_or_404(Task, id=task_id)
        
        # Cycle through statuses
        status_cycle = {
            'TODO': 'IN_PROGRESS',
            'IN_PROGRESS': 'DONE',
            'DONE': 'TODO',
            'BLOCKED': 'TODO'
        }
        
        task.status = status_cycle.get(task.status, 'TODO')
        task.save()
        
        # Return partial HTML for HTMX
        return render(request, 'partials/task_row.html', {'task': task})
    
    return JsonResponse({'error': 'Invalid request'}, status=400)


def today_view(request):
    """Today view showing urgent and high-priority tasks"""
    # Get urgent/high priority tasks that are not done
    urgent_tasks = Task.objects.filter(
        priority__in=['URGENT', 'HIGH']
    ).exclude(status='DONE').select_related('project')
    
    # Get overdue tasks
    overdue_tasks = Task.objects.filter(
        due_date__lt=timezone.now().date()
    ).exclude(status='DONE').select_related('project')
    
    # Combine and remove duplicates
    all_urgent_tasks = (urgent_tasks | overdue_tasks).distinct().order_by('-priority', 'due_date')
    
    return render(request, 'today.html', {'tasks': all_urgent_tasks})


def review_merge_queue(request):
    """Review & Merge Queue showing all open PRs across all repositories"""
    # Get all projects with GitHub repositories
    projects = Project.objects.exclude(repo_name='').exclude(repo_name__isnull=True)
    
    github = GitHubClient()
    all_prs = []
    
    for project in projects:
        prs = github.fetch_pull_requests(project.repo_name, state='open')
        for pr in prs:
            pr['project'] = project
            all_prs.append(pr)
    
    # Sort by updated_at (most recent first)
    all_prs.sort(key=lambda x: x.get('updated_at', ''), reverse=True)
    
    return render(request, 'review_merge.html', {'pull_requests': all_prs})
