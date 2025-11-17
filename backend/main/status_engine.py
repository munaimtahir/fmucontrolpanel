"""
Automatic status and risk engine for projects based on GitHub activity
"""
from datetime import datetime, timedelta
from django.utils import timezone
from .github_client import GitHubClient


class StatusEngine:
    """Engine for automatic status and risk updates"""
    
    def __init__(self, project):
        self.project = project
        self.github = GitHubClient()
    
    def update_status(self):
        """Update project status based on GitHub activity"""
        if not self.project.repo_name or not self.project.auto_status_enabled:
            return False
        
        # Fetch GitHub data
        prs = self.github.fetch_pull_requests(self.project.repo_name, state='open')
        commits = self.github.fetch_commits(self.project.repo_name, limit=10)
        
        # Determine status
        new_status = self._calculate_status(prs, commits)
        
        if new_status and new_status != self.project.status:
            self.project.status = new_status
            self.project.save()
            return True
        
        return False
    
    def update_risk(self):
        """Update project risk based on GitHub issues"""
        if not self.project.repo_name or not self.project.auto_status_enabled:
            return False
        
        # Fetch issues
        issues = self.github.fetch_issues(self.project.repo_name, state='open')
        
        # Count critical issues (those with specific labels)
        critical_count = sum(
            1 for issue in issues 
            if any(label.lower() in ['critical', 'urgent', 'blocker', 'security'] 
                   for label in issue.get('labels', []))
        )
        
        # Determine risk level
        new_risk = 'HIGH' if critical_count > 0 else (
            'MEDIUM' if len(issues) > 5 else 'LOW'
        )
        
        if new_risk != self.project.risk:
            self.project.risk = new_risk
            self.project.save()
            return True
        
        return False
    
    def _calculate_status(self, prs, commits):
        """Calculate status based on PRs and commits"""
        # Check if there are open PRs
        if prs:
            # Check if any PR has failing CI
            for pr in prs:
                # In a real implementation, you'd check PR status/checks
                # For now, we'll assume if it's a draft it might be blocked
                if pr.get('draft'):
                    return 'BLOCKED'
            
            # Has open PRs and not blocked
            return 'IN_PROGRESS'
        
        # No open PRs - check commit activity
        if commits:
            latest_commit = commits[0]
            commit_date_str = latest_commit.get('date', '')
            
            if commit_date_str:
                try:
                    # Parse ISO 8601 date
                    commit_date = datetime.fromisoformat(commit_date_str.replace('Z', '+00:00'))
                    days_since_commit = (timezone.now() - commit_date).days
                    
                    if days_since_commit > self.project.stale_days:
                        return 'STALE'
                except (ValueError, AttributeError):
                    pass
        
        # Default: keep current status or set to planning
        return None
    
    def auto_update(self):
        """Run all automatic updates"""
        status_updated = self.update_status()
        risk_updated = self.update_risk()
        
        return status_updated or risk_updated
