from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group


class Command(BaseCommand):
    help = "Create default groups and permissions"

    def handle(self, *args, **kwargs):
        moderator_group, created = Group.objects.get_or_create(name="moderator")
        if created:
            self.stdout.write(self.style.SUCCESS("Moderator group created"))
        else:
            self.stdout.write(self.style.WARNING("Moderator group already exists"))
