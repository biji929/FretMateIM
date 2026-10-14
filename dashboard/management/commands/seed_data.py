from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from dashboard.models import UserProfile, Chord, Tab, PracticeSession, UserChordProgress
from datetime import timedelta
from django.utils import timezone
import random

class Command(BaseCommand):
    help = 'Seeds database with demo data'

    def handle(self, *args, **kwargs):
        # Create demo user
        user, created = User.objects.get_or_create(username='demo_user')
        if created:
            user.set_password('password')
            user.save()
            UserProfile.objects.create(user=user, skill_level='Intermediate', weekly_goal_minutes=150)
            self.stdout.write(self.style.SUCCESS('Demo user created'))
        else:
            self.stdout.write('Demo user already exists')

        # Create chords
        genres = ['Rock', 'Jazz', 'Pop', 'Acoustic']
        difficulties = ['Easy', 'Medium', 'Hard']
        for i in range(15):
            chord, _ = Chord.objects.get_or_create(
                name=f'Chord_{i+1}',
                defaults={
                    'genre': random.choice(genres),
                    'difficulty': random.choice(difficulties),
                    'diagram_data': {"frets": [0,2,2,1,0,0], "fingers": [0,1,2,3,0,0], "base_fret": 1}
                }
            )
            UserChordProgress.objects.get_or_create(user=user, chord=chord, status=random.choice(['Learning', 'Mastered']))

        # Create tabs
        for i in range(5):
            tab, _ = Tab.objects.get_or_create(
                title=f'Tab_{i+1}',
                artist=f'Artist_{i+1}',
                defaults={
                    'genre': random.choice(genres),
                    'content': '--0--\n--1--\n--2--'
                }
            )
            # Add some chords to tab
            tab.associated_chords.set(Chord.objects.all()[:3])

        # Create practice sessions (last 45 days)
        # Using objects.bulk_create to bypass auto_now_add issue if any,
        # but setting date explicitly works for creation
        sessions = []
        for i in range(45):
            date = timezone.now().date() - timedelta(days=i)
            # Ensure streak: log every day
            session = PracticeSession(
                user=user,
                duration_minutes=random.randint(15, 60),
                focus_area=random.choice(['Chords', 'Songs', 'Scales', 'Rhythm'])
            )
            session.date = date
            sessions.append(session)

        PracticeSession.objects.bulk_create(sessions)

        self.stdout.write(self.style.SUCCESS('Database seeded successfully'))
