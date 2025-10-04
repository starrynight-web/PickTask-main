from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from workspace.models import Workspace, Membership, Project, Task, ActivityLog
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = 'Creates demo data for testing PickTask'
    
    def handle(self, *args, **options):
        self.stdout.write('Setting up demo data for PickTask...')
        
        # Create demo user
        user, created = User.objects.get_or_create(
            username='demo',
            defaults={
                'email': 'demo@picktask.com',
                'first_name': 'Demo',
                'last_name': 'User',
                'is_active': True
            }
        )
        if created:
            user.set_password('demo123')
            user.save()
            self.stdout.write(self.style.SUCCESS('✅ Created demo user: demo/demo123'))
        
        # Create demo workspace
        workspace, created = Workspace.objects.get_or_create(
            name='Development Team',
            created_by=user
        )
        if created:
            self.stdout.write(self.style.SUCCESS('✅ Created demo workspace'))
        
        # Add user as admin
        Membership.objects.get_or_create(
            user=user,
            workspace=workspace,
            role='admin'
        )
        
        # Create sample projects
        projects_data = [
            {'name': 'Website Redesign', 'color': '#3B82F6', 'description': 'Complete website overhaul with modern design'},
            {'name': 'Mobile App', 'color': '#8B5CF6', 'description': 'iOS and Android mobile application'},
            {'name': 'API Development', 'color': '#10B981', 'description': 'Backend API and database design'},
        ]
        
        for project_data in projects_data:
            project, created = Project.objects.get_or_create(
                name=project_data['name'],
                workspace=workspace,
                created_by=user,
                color=project_data['color'],
                description=project_data['description']
            )
            if created:
                self.stdout.write(f'✅ Created project: {project.name}')
                
                # Create sample tasks for each project
                tasks_data = [
                    {
                        'title': f'Design {project.name} homepage',
                        'status': 'todo',
                        'priority': 'high',
                        'description': f'Create modern design for {project.name} homepage'
                    },
                    {
                        'title': f'Implement user authentication',
                        'status': 'in_progress', 
                        'priority': 'medium',
                        'description': 'Set up secure user login and registration'
                    },
                    {
                        'title': f'Write documentation',
                        'status': 'review',
                        'priority': 'low',
                        'description': 'Create comprehensive project documentation'
                    },
                    {
                        'title': f'Testing and deployment',
                        'status': 'done',
                        'priority': 'high',
                        'description': 'Final testing and production deployment'
                    },
                ]
                
                for i, task_data in enumerate(tasks_data):
                    task = Task.objects.create(
                        title=task_data['title'],
                        description=task_data['description'],
                        project=project,
                        status=task_data['status'],
                        priority=task_data['priority'],
                        created_by=user,
                        due_date=timezone.now() + timedelta(days=i*2)
                    )
                
                # Log activity
                ActivityLog.objects.create(
                    workspace=workspace,
                    user=user,
                    action=f"created project '{project.name}' with sample tasks"
                )
        
        self.stdout.write(self.style.SUCCESS('🎉 Demo data created successfully!'))
        self.stdout.write(self.style.SUCCESS('🔑 Login with: username="demo", password="demo123"'))
        self.stdout.write(self.style.SUCCESS('🌐 Access at: http://localhost:8000'))