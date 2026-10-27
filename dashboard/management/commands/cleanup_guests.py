from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = 'Deletes guest users older than 7 days'

    def handle(self, *args, **kwargs):
        cutoff = timezone.now() - timedelta(days=7)
        old_guests = User.objects.filter(username__startswith='guest_', date_joined__lt=cutoff)
        count, _ = old_guests.delete()
        self.stdout.write(self.style.SUCCESS(f'Successfully deleted {count} guest user(s) older than 7 days.'))
