"""
GitHub webhook handler for real-time project updates
"""
import json
import hmac
import hashlib
from django.conf import settings
from django.utils import timezone
from .models import Project, Task, LogEntry
from .status_engine import StatusEngine


class WebhookHandler:
    """Handler for GitHub webhook events"""
    
    @staticmethod
    def verify_signature(payload_body, signature):
        """Verify webhook signature from GitHub"""
        if not signature:
            return False
        
        # GitHub sends signature as 'sha256=...'
        if not signature.startswith('sha256='):
            return False
        
        expected_signature = signature.split('=')[1]
        
        # Calculate HMAC
        secret = settings.GITHUB_WEBHOOK_SECRET.encode() if hasattr(settings, 'GITHUB_WEBHOOK_SECRET') else b''
        mac = hmac.new(secret, msg=payload_body, digestmod=hashlib.sha256)
        calculated_signature = mac.hexdigest()
        
        return hmac.compare_digest(expected_signature, calculated_signature)
    
    @staticmethod
    def handle_pull_request(data):
        """Handle pull_request webhook event"""
        action = data.get('action')
        pr = data.get('pull_request', {})
        repo_full_name = data.get('repository', {}).get('full_name')
        
        if not repo_full_name:
            return False
        
        # Find project with this repository
        try:
            project = Project.objects.get(repo_name=repo_full_name)
        except Project.DoesNotExist:
            return False
        
        # Log the PR event
        pr_number = pr.get('number')
        pr_title = pr.get('title')
        pr_user = pr.get('user', {}).get('login', 'unknown')
        
        message = f"PR #{pr_number} {action}: {pr_title} by {pr_user}"
        LogEntry.objects.create(project=project, message=message)
        
        # Update project status if auto-enabled
        if project.auto_status_enabled:
            engine = StatusEngine(project)
            engine.auto_update()
        
        return True
    
    @staticmethod
    def handle_issues(data):
        """Handle issues webhook event"""
        action = data.get('action')
        issue = data.get('issue', {})
        repo_full_name = data.get('repository', {}).get('full_name')
        
        if not repo_full_name:
            return False
        
        # Find project with this repository
        try:
            project = Project.objects.get(repo_name=repo_full_name)
        except Project.DoesNotExist:
            return False
        
        # Get issue details
        issue_number = issue.get('number')
        issue_title = issue.get('title')
        issue_user = issue.get('user', {}).get('login', 'unknown')
        issue_labels = [label.get('name') for label in issue.get('labels', [])]
        
        # Log the issue event
        message = f"Issue #{issue_number} {action}: {issue_title} by {issue_user}"
        LogEntry.objects.create(project=project, message=message)
        
        # Handle issue-to-task sync if enabled
        if project.auto_sync_issues:
            WebhookHandler._sync_issue_to_task(project, action, issue)
        
        # Update project risk if auto-enabled
        if project.auto_status_enabled:
            engine = StatusEngine(project)
            engine.update_risk()
        
        return True
    
    @staticmethod
    def handle_workflow_run(data):
        """Handle workflow_run webhook event"""
        action = data.get('action')
        workflow_run = data.get('workflow_run', {})
        repo_full_name = data.get('repository', {}).get('full_name')
        
        if not repo_full_name:
            return False
        
        # Find project with this repository
        try:
            project = Project.objects.get(repo_name=repo_full_name)
        except Project.DoesNotExist:
            return False
        
        # Get workflow details
        workflow_name = workflow_run.get('name', 'Unknown')
        conclusion = workflow_run.get('conclusion')
        status = workflow_run.get('status')
        
        # Log the workflow event
        message = f"Workflow '{workflow_name}' {action}"
        if conclusion:
            message += f" with conclusion: {conclusion}"
        elif status:
            message += f" with status: {status}"
        
        LogEntry.objects.create(project=project, message=message)
        
        # If workflow failed and project has auto-status, set to BLOCKED
        if conclusion == 'failure' and project.auto_status_enabled:
            project.status = 'BLOCKED'
            project.save()
        
        return True
    
    @staticmethod
    def _sync_issue_to_task(project, action, issue):
        """Sync GitHub issue to task"""
        issue_number = issue.get('number')
        issue_title = issue.get('title')
        issue_body = issue.get('body', '')
        issue_labels = [label.get('name') for label in issue.get('labels', [])]
        
        # Determine priority from labels
        priority = 'MEDIUM'
        if any(label.lower() in ['critical', 'urgent'] for label in issue_labels):
            priority = 'URGENT'
        elif any(label.lower() == 'high' for label in issue_labels):
            priority = 'HIGH'
        elif any(label.lower() == 'low' for label in issue_labels):
            priority = 'LOW'
        
        # Create or update task based on action
        if action == 'opened':
            # Create new task
            Task.objects.create(
                project=project,
                title=f"GH Issue #{issue_number}: {issue_title}",
                description=issue_body[:500] if issue_body else '',  # Limit description
                status='TODO',
                priority=priority
            )
        
        elif action == 'closed':
            # Mark corresponding task as DONE
            tasks = Task.objects.filter(
                project=project,
                title__contains=f"GH Issue #{issue_number}"
            )
            tasks.update(status='DONE')
        
        elif action == 'reopened':
            # Reopen corresponding task
            tasks = Task.objects.filter(
                project=project,
                title__contains=f"GH Issue #{issue_number}"
            )
            tasks.update(status='TODO')
