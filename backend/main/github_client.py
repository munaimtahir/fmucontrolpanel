"""
GitHub API client for fetching repository data
"""
import requests
from django.conf import settings
from typing import List, Dict, Optional


class GitHubClient:
    """Client for interacting with GitHub API"""
    
    BASE_URL = "https://api.github.com"
    
    def __init__(self, token: Optional[str] = None):
        self.token = token or settings.GITHUB_TOKEN
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
        }
        if self.token:
            self.headers["Authorization"] = f"token {self.token}"
    
    def _get(self, endpoint: str, params: Optional[Dict] = None) -> Optional[Dict]:
        """Make a GET request to GitHub API"""
        try:
            url = f"{self.BASE_URL}/{endpoint}"
            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"GitHub API error: {e}")
            return None
    
    def fetch_pull_requests(self, repo_name: str, state: str = "open") -> List[Dict]:
        """
        Fetch pull requests for a repository
        
        Args:
            repo_name: Repository in format 'owner/repo'
            state: PR state - 'open', 'closed', or 'all'
        
        Returns:
            List of pull request dictionaries
        """
        if not repo_name:
            return []
        
        endpoint = f"repos/{repo_name}/pulls"
        params = {"state": state, "per_page": 10}
        data = self._get(endpoint, params)
        
        if not data:
            return []
        
        # Extract relevant PR information
        prs = []
        for pr in data:
            prs.append({
                'number': pr.get('number'),
                'title': pr.get('title'),
                'state': pr.get('state'),
                'user': pr.get('user', {}).get('login'),
                'created_at': pr.get('created_at'),
                'updated_at': pr.get('updated_at'),
                'html_url': pr.get('html_url'),
                'draft': pr.get('draft', False),
            })
        
        return prs
    
    def fetch_commits(self, repo_name: str, limit: int = 10) -> List[Dict]:
        """
        Fetch recent commits for a repository
        
        Args:
            repo_name: Repository in format 'owner/repo'
            limit: Number of commits to fetch (default: 10)
        
        Returns:
            List of commit dictionaries
        """
        if not repo_name:
            return []
        
        endpoint = f"repos/{repo_name}/commits"
        params = {"per_page": limit}
        data = self._get(endpoint, params)
        
        if not data:
            return []
        
        # Extract relevant commit information
        commits = []
        for commit in data:
            commits.append({
                'sha': commit.get('sha', '')[:7],  # Short SHA
                'message': commit.get('commit', {}).get('message', '').split('\n')[0],  # First line only
                'author': commit.get('commit', {}).get('author', {}).get('name'),
                'date': commit.get('commit', {}).get('author', {}).get('date'),
                'html_url': commit.get('html_url'),
            })
        
        return commits
    
    def fetch_issues(self, repo_name: str, state: str = "open") -> List[Dict]:
        """
        Fetch issues for a repository
        
        Args:
            repo_name: Repository in format 'owner/repo'
            state: Issue state - 'open', 'closed', or 'all'
        
        Returns:
            List of issue dictionaries
        """
        if not repo_name:
            return []
        
        endpoint = f"repos/{repo_name}/issues"
        params = {"state": state, "per_page": 10}
        data = self._get(endpoint, params)
        
        if not data:
            return []
        
        # Extract relevant issue information (filter out PRs)
        issues = []
        for issue in data:
            # Skip pull requests (they appear in issues endpoint too)
            if 'pull_request' in issue:
                continue
            
            issues.append({
                'number': issue.get('number'),
                'title': issue.get('title'),
                'state': issue.get('state'),
                'user': issue.get('user', {}).get('login'),
                'created_at': issue.get('created_at'),
                'updated_at': issue.get('updated_at'),
                'html_url': issue.get('html_url'),
                'labels': [label.get('name') for label in issue.get('labels', [])],
            })
        
        return issues
    
    def fetch_repo_info(self, repo_name: str) -> Optional[Dict]:
        """
        Fetch basic repository information
        
        Args:
            repo_name: Repository in format 'owner/repo'
        
        Returns:
            Repository information dictionary
        """
        if not repo_name:
            return None
        
        endpoint = f"repos/{repo_name}"
        data = self._get(endpoint)
        
        if not data:
            return None
        
        return {
            'name': data.get('name'),
            'full_name': data.get('full_name'),
            'description': data.get('description'),
            'html_url': data.get('html_url'),
            'stars': data.get('stargazers_count'),
            'forks': data.get('forks_count'),
            'open_issues': data.get('open_issues_count'),
            'default_branch': data.get('default_branch'),
        }
