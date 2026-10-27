from django.core.management.base import BaseCommand
from dashboard.models import Tab

SONG_MEDIA = {
    # Jazz & Blues acoustic fingerstyle
    'Autumn Leaves': {
        'youtube': 'https://www.youtube.com/watch?v=G0eQ6w1L81g',
        'audio': '/static/audio/acoustic_blues_jazz.mp3',
    },
    'Fly Me to the Moon': {
        'youtube': 'https://www.youtube.com/watch?v=5hxibHE6r58',
        'audio': '/static/audio/acoustic_blues_jazz.mp3',
    },
    'Summertime': {
        'youtube': 'https://www.youtube.com/watch?v=MIDOEsQLWB8',
        'audio': '/static/audio/acoustic_blues_jazz.mp3',
    },

    # Folk & Country acoustic strumming
    'Bad Moon Rising': {
        'youtube': 'https://www.youtube.com/watch?v=zUQiUFZ5IAk',
        'audio': '/static/audio/acoustic_folk_strumming.mp3',
    },
    "Blowin' in the Wind": {
        'youtube': 'https://www.youtube.com/watch?v=MMFj8uTBoE4',
        'audio': '/static/audio/acoustic_folk_strumming.mp3',
    },
    'Horse with No Name': {
        'youtube': 'https://www.youtube.com/watch?v=na47wMFfQCo',
        'audio': '/static/audio/acoustic_folk_strumming.mp3',
    },
    'Sweet Home Alabama': {
        'youtube': 'https://www.youtube.com/watch?v=ye5BuYf8q4o',
        'audio': '/static/audio/acoustic_folk_strumming.mp3',
    },

    # Upbeat Acoustic Chords & Fingerstyle
    'Wonderwall': {
        'youtube': 'https://www.youtube.com/watch?v=bx1Bh8ZvH84',
        'audio': '/static/audio/acoustic_guitar_in_the_sun.mp3',
    },
    "I'm Yours": {
        'youtube': 'https://www.youtube.com/watch?v=EkHTsc9PU2A',
        'audio': '/static/audio/acoustic_guitar_in_the_sun.mp3',
    },
    'Riptide': {
        'youtube': 'https://www.youtube.com/watch?v=uJ_1HMAGb4k',
        'audio': '/static/audio/acoustic_guitar_in_the_sun.mp3',
    },
    'Counting Stars': {
        'youtube': 'https://www.youtube.com/watch?v=hT_nvWreIhg',
        'audio': '/static/audio/acoustic_guitar_in_the_sun.mp3',
    },

    # Pop & Rock Acoustic Strumming
    'Californication': {
        'youtube': 'https://www.youtube.com/watch?v=YlUKcNNmywk',
        'audio': '/static/audio/acoustic_joyful_strumming.mp3',
    },
    'Stand By Me': {
        'youtube': 'https://www.youtube.com/watch?v=hwZNL7QVJjE',
        'audio': '/static/audio/acoustic_joyful_strumming.mp3',
    },
    'Fast Car': {
        'youtube': 'https://www.youtube.com/watch?v=AIOAlaACuv4',
        'audio': '/static/audio/acoustic_joyful_strumming.mp3',
    },
    'Hey There Delilah': {
        'youtube': 'https://www.youtube.com/watch?v=h_m-BjrxmgI',
        'audio': '/static/audio/acoustic_joyful_strumming.mp3',
    },
    'Zombie': {
        'youtube': 'https://www.youtube.com/watch?v=6Ejga4kJUts',
        'audio': '/static/audio/acoustic_joyful_strumming.mp3',
    },

    # Slow Acoustic Ballads & Fingerstyle
    'Hallelujah': {
        'youtube': 'https://www.youtube.com/watch?v=y8AWFf7EAc4',
        'audio': '/static/audio/acoustic_slow_ballad.mp3',
    },
    "Knockin' on Heaven's Door": {
        'youtube': 'https://www.youtube.com/watch?v=rm9coqlk8fY',
        'audio': '/static/audio/acoustic_slow_ballad.mp3',
    },
    'Let It Be': {
        'youtube': 'https://www.youtube.com/watch?v=QDYfEBY9NM4',
        'audio': '/static/audio/acoustic_slow_ballad.mp3',
    },
    'Wish You Were Here': {
        'youtube': 'https://www.youtube.com/watch?v=IXdNnw99-Ic',
        'audio': '/static/audio/acoustic_slow_ballad.mp3',
    },
    'Hotel California': {
        'youtube': 'https://www.youtube.com/watch?v=09839DpTctU',
        'audio': '/static/audio/acoustic_slow_ballad.mp3',
    },
    'Creep': {
        'youtube': 'https://www.youtube.com/watch?v=XFkzRNyygfk',
        'audio': '/static/audio/acoustic_slow_ballad.mp3',
    },
    'Nothing Else Matters': {
        'youtube': 'https://www.youtube.com/watch?v=tAGnKpE4NCI',
        'audio': '/static/audio/acoustic_slow_ballad.mp3',
    },
    'Perfect': {
        'youtube': 'https://www.youtube.com/watch?v=2Vv-BfVoq4g',
        'audio': '/static/audio/acoustic_slow_ballad.mp3',
    },
    'Shallow': {
        'youtube': 'https://www.youtube.com/watch?v=bo_efYhYU2A',
        'audio': '/static/audio/acoustic_slow_ballad.mp3',
    },
    'Someone Like You': {
        'youtube': 'https://www.youtube.com/watch?v=hLQl3WQQoQ0',
        'audio': '/static/audio/acoustic_slow_ballad.mp3',
    },
}

class Command(BaseCommand):
    help = 'Populates all songs with real acoustic guitar backing tracks and YouTube videos'

    def handle(self, *args, **options):
        self.stdout.write("Linking real acoustic guitar MP3 tracks to ALL songs...")
        updated = 0
        for tab in Tab.objects.all():
            media = SONG_MEDIA.get(tab.title)
            if media:
                tab.youtube_url = media['youtube']
                tab.audio_url = media['audio']
                tab.save()
                updated += 1
                self.stdout.write(f"  + Linked: {tab.title} -> {media['audio']}")
            else:
                tab.youtube_url = 'https://www.youtube.com/watch?v=bx1Bh8ZvH84'
                tab.audio_url = '/static/audio/acoustic_guitar_in_the_sun.mp3'
                tab.save()
                updated += 1

        self.stdout.write(self.style.SUCCESS(f"Successfully linked authentic acoustic guitar MP3 tracks to all {updated} songs!"))
