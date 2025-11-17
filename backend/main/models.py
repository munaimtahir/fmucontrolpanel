from django.db import models
from django.utils import timezone


class Project(models.Model):
    """Main project model for FMU Control Panel"""
    
    STATUS_CHOICES = [
        ('PLANNING', 'Planning'),
        ('IN_PROGRESS', 'In Progress'),
        ('BLOCKED', 'Blocked'),
        ('STALE', 'Stale'),
        ('COMPLETED', 'Completed'),
    ]
    
    RISK_CHOICES = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
    ]
    
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PLANNING')
    risk = models.CharField(max_length=10, choices=RISK_CHOICES, default='LOW')
    summary = models.TextField(blank=True, help_text="Brief project summary")
    next_task = models.CharField(max_length=200, blank=True, help_text="Next immediate action")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-updated_at']
    
    def __str__(self):
        return self.name
    
    @property
    def open_tasks_count(self):
        return self.tasks.exclude(status='DONE').count()


class Task(models.Model):
    """Task model linked to projects"""
    
    STATUS_CHOICES = [
        ('TODO', 'To Do'),
        ('IN_PROGRESS', 'In Progress'),
        ('DONE', 'Done'),
        ('BLOCKED', 'Blocked'),
    ]
    
    PRIORITY_CHOICES = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
        ('URGENT', 'Urgent'),
    ]
    
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='TODO')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='MEDIUM')
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-priority', 'due_date', '-created_at']
    
    def __str__(self):
        return f"{self.project.name} - {self.title}"
    
    @property
    def is_urgent(self):
        """Check if task is urgent based on priority or due date"""
        if self.priority == 'URGENT':
            return True
        if self.due_date and self.due_date <= timezone.now().date():
            return True
        return False


class Link(models.Model):
    """Link model for project resources"""
    
    LINK_TYPE_CHOICES = [
        ('GITHUB', 'GitHub Repository'),
        ('DOCS', 'Documentation'),
        ('DEPLOYMENT', 'Deployment'),
        ('OTHER', 'Other'),
    ]
    
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='links')
    title = models.CharField(max_length=200)
    url = models.URLField()
    link_type = models.CharField(max_length=20, choices=LINK_TYPE_CHOICES, default='OTHER')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['link_type', 'title']
    
    def __str__(self):
        return f"{self.project.name} - {self.title}"


class LogEntry(models.Model):
    """Log entry model for project activity tracking"""
    
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='logs')
    message = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-timestamp']
        verbose_name_plural = 'Log entries'
    
    def __str__(self):
        return f"{self.project.name} - {self.timestamp.strftime('%Y-%m-%d %H:%M')}"
