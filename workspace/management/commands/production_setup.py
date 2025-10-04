from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from workspace.models import Workspace, Membership

class Command(BaseCommand):
    help = 'Initial setup for production deployment'
    
    def handle(self, *args, **options):
        # Create initial workspace for admin user
        admin_user = User.objects.filter(is_superuser=True).first()
        if admin_user and not Workspace.objects.exists():
            workspace = Workspace.objects.create(
                name='My Workspace',
                created_by=admin_user
            )
            Membership.objects.create(
                user=admin_user,
                workspace=workspace,
                role='admin'
            )
            self.stdout.write(
                self.style.SUCCESS('✅ Initial workspace created for admin!')
            )