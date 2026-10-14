from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import PracticeSession, Chord, UserProfile
from django.urls import reverse

class FretMateTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client = Client()
        self.client.login(username='testuser', password='password')

    def test_auth_protection(self):
        self.client.logout()
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)

    def test_logger_ajax(self):
        response = self.client.post(reverse('logger'), {
            'duration_minutes': 30,
            'focus_area': 'Chords',
            'notes': 'test notes'
        })
        self.assertEqual(response.status_code, 201)
        self.assertTrue(PracticeSession.objects.filter(user=self.user).exists())

    def test_data_isolation(self):
        user2 = User.objects.create_user(username='user2', password='password')
        PracticeSession.objects.create(user=self.user, duration_minutes=10, focus_area='Chords')
        PracticeSession.objects.create(user=user2, duration_minutes=20, focus_area='Chords')
        self.assertEqual(PracticeSession.objects.filter(user=self.user).count(), 1)
        self.assertEqual(PracticeSession.objects.filter(user=user2).count(), 1)
