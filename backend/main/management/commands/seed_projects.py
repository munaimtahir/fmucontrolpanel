from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from main.models import Project, Task, Link, LogEntry


class Command(BaseCommand):
    help = 'Seed the database with 5 FMU projects and sample data'

    def handle(self, *args, **options):
        self.stdout.write('Seeding FMU projects...')
        
        # Clear existing data
        Project.objects.all().delete()
        
        # Project 1: FMU Consultation System
        project1 = Project.objects.create(
            name='FMU Consultation System',
            description='Web-based consultation system for FMU clients to schedule and manage appointments.',
            repo_name='fmu/consultation-system',
            status='IN_PROGRESS',
            risk='MEDIUM',
            summary='Backend API complete, frontend integration in progress. Expected completion next month.',
            next_task='Complete user authentication flow'
        )
        Task.objects.create(
            project=project1,
            title='Implement user authentication',
            status='IN_PROGRESS',
            priority='HIGH',
            due_date=timezone.now().date() + timedelta(days=3)
        )
        Task.objects.create(
            project=project1,
            title='Create appointment scheduling UI',
            status='TODO',
            priority='MEDIUM',
            due_date=timezone.now().date() + timedelta(days=7)
        )
        Link.objects.create(
            project=project1,
            title='GitHub Repository',
            url='https://github.com/fmu/consultation-system',
            link_type='GITHUB'
        )
        LogEntry.objects.create(
            project=project1,
            message='Backend API endpoints completed and tested'
        )
        
        # Project 2: FMU Website
        project2 = Project.objects.create(
            name='FMU Website',
            description='Main FMU corporate website with service information and contact forms.',
            repo_name='fmu/website',
            status='IN_PROGRESS',
            risk='LOW',
            summary='Content updates ongoing. New landing page design approved.',
            next_task='Deploy new landing page design'
        )
        Task.objects.create(
            project=project2,
            title='Update homepage with new design',
            status='IN_PROGRESS',
            priority='HIGH',
            due_date=timezone.now().date() + timedelta(days=2)
        )
        Task.objects.create(
            project=project2,
            title='Add blog section',
            status='TODO',
            priority='LOW',
            due_date=timezone.now().date() + timedelta(days=14)
        )
        Link.objects.create(
            project=project2,
            title='Production Website',
            url='https://www.fmu.example.com',
            link_type='DEPLOYMENT'
        )
        Link.objects.create(
            project=project2,
            title='GitHub Repository',
            url='https://github.com/fmu/website',
            link_type='GITHUB'
        )
        LogEntry.objects.create(
            project=project2,
            message='New landing page design approved by stakeholders'
        )
        
        # Project 3: SIMS
        project3 = Project.objects.create(
            name='SIMS',
            description='Student Information Management System for tracking academic records and enrollment.',
            repo_name='fmu/sims',
            status='PLANNING',
            risk='HIGH',
            summary='Requirements gathering phase. Database schema being finalized.',
            next_task='Finalize database schema and ERD'
        )
        Task.objects.create(
            project=project3,
            title='Complete database schema design',
            status='IN_PROGRESS',
            priority='URGENT',
            due_date=timezone.now().date() + timedelta(days=1)
        )
        Task.objects.create(
            project=project3,
            title='Define API specifications',
            status='TODO',
            priority='HIGH',
            due_date=timezone.now().date() + timedelta(days=5)
        )
        Link.objects.create(
            project=project3,
            title='Requirements Document',
            url='https://docs.google.com/document/sims-requirements',
            link_type='DOCS'
        )
        LogEntry.objects.create(
            project=project3,
            message='Initial requirements gathering meeting completed'
        )
        
        # Project 4: Google Workspace
        project4 = Project.objects.create(
            name='Google Workspace',
            description='Google Workspace administration and integration for FMU organization.',
            repo_name='',  # No GitHub repo for this project
            status='COMPLETED',
            risk='LOW',
            summary='All users migrated successfully. SSO configured and working.',
            next_task='Monitor usage and provide support'
        )
        Task.objects.create(
            project=project4,
            title='User training sessions',
            status='DONE',
            priority='MEDIUM'
        )
        Task.objects.create(
            project=project4,
            title='Configure backup policies',
            status='DONE',
            priority='MEDIUM'
        )
        Link.objects.create(
            project=project4,
            title='Admin Console',
            url='https://admin.google.com',
            link_type='OTHER'
        )
        Link.objects.create(
            project=project4,
            title='Setup Documentation',
            url='https://docs.google.com/workspace-setup',
            link_type='DOCS'
        )
        LogEntry.objects.create(
            project=project4,
            message='All 150 users successfully migrated to Google Workspace'
        )
        
        # Project 5: SIMS/Workspace Database & Sync
        project5 = Project.objects.create(
            name='SIMS/Workspace Database & Sync',
            description='Integration between SIMS and Google Workspace for automated user provisioning.',
            repo_name='fmu/workspace-sync',
            status='BLOCKED',
            risk='HIGH',
            summary='Waiting for SIMS database schema finalization. Sync architecture designed.',
            next_task='Wait for SIMS schema completion before proceeding'
        )
        Task.objects.create(
            project=project5,
            title='Design sync architecture',
            status='DONE',
            priority='HIGH'
        )
        Task.objects.create(
            project=project5,
            title='Implement data sync service',
            status='BLOCKED',
            priority='HIGH',
            due_date=timezone.now().date() + timedelta(days=10)
        )
        Link.objects.create(
            project=project5,
            title='Architecture Diagram',
            url='https://docs.google.com/drawings/sync-architecture',
            link_type='DOCS'
        )
        LogEntry.objects.create(
            project=project5,
            message='Sync architecture approved. Blocked on SIMS completion.'
        )
        
        self.stdout.write(self.style.SUCCESS(f'Successfully seeded 5 projects with tasks, links, and logs'))
