from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from workspace.models import Workspace, Membership, Project, Task, ActivityLog
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = 'Creates comprehensive demo data for PickTask'
    
    def handle(self, *args, **options):
        self.stdout.write('Creating comprehensive demo data for PickTask...')
        
        # Create demo users
        users_data = [
            {'username': 'admin', 'email': 'admin@picktask.com', 'first_name': 'System', 'last_name': 'Admin'},
            {'username': 'pm_alex', 'email': 'alex@company.com', 'first_name': 'Alex', 'last_name': 'Johnson'},
            {'username': 'dev_sam', 'email': 'sam@company.com', 'first_name': 'Sam', 'last_name': 'Chen'},
            {'username': 'design_taylor', 'email': 'taylor@company.com', 'first_name': 'Taylor', 'last_name': 'Reed'},
        ]
        
        users = {}
        for user_data in users_data:
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults=user_data
            )
            if created:
                user.set_password('demo123')
                user.save()
                self.stdout.write(f"✅ Created user: {user.username}")
            users[user_data['username']] = user
        
        # Create multiple workspaces
        workspaces_data = [
            {
                'name': 'Web Development Team', 
                'description': 'Main website and application development'
            },
            {
                'name': 'Mobile App Project', 
                'description': 'iOS and Android mobile application development'
            },
            {
                'name': 'Marketing Department', 
                'description': 'Content creation and campaign management'
            },
        ]
        
        workspaces = {}
        for i, ws_data in enumerate(workspaces_data):
            workspace, created = Workspace.objects.get_or_create(
                name=ws_data['name'],
                created_by=users['admin'],
                defaults=ws_data
            )
            if created:
                self.stdout.write(f"✅ Created workspace: {workspace.name}")
            
            # Add members with different roles
            memberships_data = [
                {'user': users['admin'], 'role': 'admin'},
                {'user': users['pm_alex'], 'role': 'admin'},
                {'user': users['dev_sam'], 'role': 'member'},
                {'user': users['design_taylor'], 'role': 'member'},
            ]
            
            for membership_data in memberships_data:
                Membership.objects.get_or_create(
                    user=membership_data['user'],
                    workspace=workspace,
                    role=membership_data['role']
                )
            
            workspaces[ws_data['name']] = workspace
            
            # Create projects for each workspace
            if i == 0:  # Web Development Team
                projects_data = [
                    {'name': 'Website Redesign', 'color': '#3B82F6', 'description': 'Complete website overhaul with modern design system'},
                    {'name': 'E-commerce Platform', 'color': '#8B5CF6', 'description': 'Online store with payment integration'},
                    {'name': 'Customer Portal', 'color': '#10B981', 'description': 'Client-facing dashboard and portal'},
                ]
            elif i == 1:  # Mobile App Project
                projects_data = [
                    {'name': 'iOS App Development', 'color': '#000000', 'description': 'Native iOS application for iPhone and iPad'},
                    {'name': 'Android App', 'color': '#34D399', 'description': 'Native Android application development'},
                    {'name': 'Backend API', 'color': '#F59E0B', 'description': 'REST API for mobile applications'},
                ]
            else:  # Marketing Department
                projects_data = [
                    {'name': 'Q4 Campaign', 'color': '#EF4444', 'description': 'End of year marketing campaign'},
                    {'name': 'Social Media', 'color': '#EC4899', 'description': 'Social media content and scheduling'},
                    {'name': 'Blog Content', 'color': '#6366F1', 'description': 'Weekly blog posts and articles'},
                ]
            
            for project_data in projects_data:
                project, created = Project.objects.get_or_create(
                    name=project_data['name'],
                    workspace=workspace,
                    created_by=users['pm_alex'],
                    color=project_data['color'],
                    description=project_data['description']
                )
                
                if created:
                    self.stdout.write(f"   ✅ Created project: {project.name}")
                    
                    # Create comprehensive tasks for each project
                    tasks_data = self.get_tasks_data(project.name)
                    
                    for j, task_data in enumerate(tasks_data):
                        task = Task.objects.create(
                            title=task_data['title'],
                            description=task_data['description'],
                            project=project,
                            status=task_data['status'],
                            priority=task_data['priority'],
                            assigned_to=task_data.get('assigned_to'),
                            due_date=timezone.now() + timedelta(days=task_data['due_days']),
                            created_by=users['pm_alex']
                        )
                        
                        # Log activity for task creation
                        ActivityLog.objects.create(
                            workspace=workspace,
                            user=users['pm_alex'],
                            action=f"created task '{task.title}' in {project.name}"
                        )
        
        self.stdout.write(self.style.SUCCESS('🎉 Comprehensive demo data created successfully!'))
        self.stdout.write(self.style.SUCCESS('🔑 Login with any demo user: username="pm_alex", "dev_sam", "design_taylor"'))
        self.stdout.write(self.style.SUCCESS('🔑 Admin login: username="admin", password="demo123"'))
        self.stdout.write(self.style.SUCCESS('🌐 Access at: http://localhost:8000'))
    
    def get_tasks_data(self, project_name):
        """Generate appropriate tasks based on project type"""
        base_tasks = [
            # Planning and Design phase
            {
                'title': f'Project kickoff and requirements gathering',
                'description': f'Initial meeting to define scope and requirements for {project_name}',
                'status': 'done',
                'priority': 'high',
                'assigned_to': None,
                'due_days': -7
            },
            {
                'title': f'Create technical specifications',
                'description': f'Document technical requirements and architecture for {project_name}',
                'status': 'done',
                'priority': 'high',
                'assigned_to': None,
                'due_days': -5
            },
            {
                'title': f'Design system setup',
                'description': f'Establish design tokens, components, and guidelines',
                'status': 'in_progress',
                'priority': 'high',
                'assigned_to': 'design_taylor',
                'due_days': 3
            },
            
            # Development phase
            {
                'title': f'Setup development environment',
                'description': f'Configure local development setup and CI/CD pipeline',
                'status': 'done',
                'priority': 'medium',
                'assigned_to': 'dev_sam',
                'due_days': -3
            },
            {
                'title': f'Implement core functionality',
                'description': f'Develop main features and business logic',
                'status': 'in_progress',
                'priority': 'high',
                'assigned_to': 'dev_sam',
                'due_days': 7
            },
            {
                'title': f'Create database schema',
                'description': f'Design and implement database structure',
                'status': 'in_progress',
                'priority': 'high',
                'assigned_to': 'dev_sam',
                'due_days': 5
            },
            
            # Testing and Review phase
            {
                'title': f'Write unit tests',
                'description': f'Create comprehensive test coverage',
                'status': 'review',
                'priority': 'medium',
                'assigned_to': 'dev_sam',
                'due_days': 10
            },
            {
                'title': f'User acceptance testing',
                'description': f'Coordinate UAT with stakeholders',
                'status': 'todo',
                'priority': 'medium',
                'assigned_to': 'pm_alex',
                'due_days': 14
            },
            {
                'title': f'Performance testing',
                'description': f'Load testing and performance optimization',
                'status': 'todo',
                'priority': 'low',
                'assigned_to': 'dev_sam',
                'due_days': 12
            },
            
            # Deployment phase
            {
                'title': f'Production deployment',
                'description': f'Deploy to production environment',
                'status': 'todo',
                'priority': 'urgent',
                'assigned_to': 'dev_sam',
                'due_days': 21
            },
            {
                'title': f'Documentation finalization',
                'description': f'Complete user and technical documentation',
                'status': 'todo',
                'priority': 'medium',
                'assigned_to': 'pm_alex',
                'due_days': 18
            },
        ]
        
        return base_tasks