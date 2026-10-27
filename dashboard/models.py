import json
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    SKILL_LEVELS = [('Beginner', 'Beginner'), ('Intermediate', 'Intermediate'), ('Advanced', 'Advanced')]
    skill_level = models.CharField(max_length=20, choices=SKILL_LEVELS, default='Beginner')
    weekly_goal_minutes = models.IntegerField(default=120, validators=[MinValueValidator(10), MaxValueValidator(3000)])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class Chord(models.Model):
    name = models.CharField(max_length=50, unique=True)
    GENRES = [('Rock', 'Rock'), ('Jazz', 'Jazz'), ('Pop', 'Pop'), ('Acoustic', 'Acoustic')]
    genre = models.CharField(max_length=20, choices=GENRES)
    DIFFICULTIES = [('Easy', 'Easy'), ('Medium', 'Medium'), ('Hard', 'Hard')]
    difficulty = models.CharField(max_length=20, choices=DIFFICULTIES)
    diagram_data = models.JSONField()  # e.g., {"frets": [0,2,2,1,0,0], "fingers": [0,1,2,3,0,0], "base_fret": 1}

    def __str__(self):
        return self.name

    @property
    def diagram_json(self):
        return json.dumps(self.diagram_data)

class Tab(models.Model):
    title = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)
    genre = models.CharField(max_length=20, choices=Chord.GENRES)
    difficulty = models.CharField(max_length=20, choices=Chord.DIFFICULTIES, default='Easy')
    key = models.CharField(max_length=10, default='C')
    content = models.TextField()
    associated_chords = models.ManyToManyField(Chord)

    def __str__(self):
        return f"{self.title} by {self.artist}"

class PracticeSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    duration_minutes = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(600)])
    FOCUS_AREAS = [('Chords', 'Chords'), ('Songs', 'Songs'), ('Scales', 'Scales'), ('Rhythm', 'Rhythm')]
    focus_area = models.CharField(max_length=20, choices=FOCUS_AREAS)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.date} - {self.duration_minutes}m"

class UserChordProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chord = models.ForeignKey(Chord, on_delete=models.CASCADE)
    STATUSES = [('Learning', 'Learning'), ('Mastered', 'Mastered')]
    status = models.CharField(max_length=20, choices=STATUSES, default='Learning')

    class Meta:
        unique_together = ('user', 'chord')

    def __str__(self):
        return f"{self.user.username} - {self.chord.name} - {self.status}"
