from django.core.management.base import BaseCommand
from dashboard.models import Tab

SONG_MEDIA = {
    'Autumn Leaves': {
        'youtube': 'https://www.youtube.com/watch?v=G0eQ6w1L81g',
        'audio': 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3',
    },
    'Bad Moon Rising': {
        'youtube': 'https://www.youtube.com/watch?v=zUQiUFZ5IAk',
        'audio': 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-3.mp3',
    },
    "Blowin' in the Wind": {
        'youtube': 'https://www.youtube.com/watch?v=MMFj8uTBoE4',
        'audio': 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-4.mp3',
    },
    'Californication': {
        'youtube': 'https://www.youtube.com/watch?v=YlUKcNNmywk',
        'audio': 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-5.mp3',
    },
    'Counting Stars': {
        'youtube': 'https://www.youtube.com/watch?v=hT_nvWreIhg',
        'audio': 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-6.mp3',
    },
    'Creep': {
        'youtube': 'https://www.youtube.com/watch?v=XFkzRNyygfk',
        'audio': 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-7.mp3',
    },
    'Fast Car': {
        'youtube': 'https://www.youtube.com/watch?v=AIOAlaACuv4',
        'audio': 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-8.mp3',
    },
    'Fly Me to the Moon': {
        'youtube': 'https://www.youtube.com/watch?v=5hxibHE6r58',
        'audio': 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-9.mp3',
    },
    'Hallelujah': {
        'youtube': 'https://www.youtube.com/watch?v=y8AWFf7EAc4',
        'audio': 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-10.mp3',
    },
    'Hey There Delilah': {
        'youtube': 'https://www.youtube.com/watch?v=h_m-BjrxmgI',
        'audio': 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-11.mp3',
    },
    'Horse with No Name': {
        'youtube': 'https://www.youtube.com/watch?v=na47wMFfQCo',
        'audio': 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-12.mp3',
    },
    'Hotel California': {
        'youtube': 'https://www.youtube.com/watch?v=09839DpTctU',
        'audio': 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-13.mp3',
    },
    "I'm Yours": {
        'youtube': 'https://www.youtube.com/watch?v=EkHTsc9PU2A',
        'audio': 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-14.mp3',
    },
    "Knockin' on Heaven's Door": {
        'youtube': 'https://www.youtube.com/watch?v=rm9coqlk8fY',
        'audio': 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-15.mp3',
    },
    'Let It Be': {
        'youtube': 'https://www.youtube.com/watch?v=QDYfEBY9NM4',
        'audio': 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-16.mp3',
    },
    'Nothing Else Matters': {
        'youtube': 'https://www.youtube.com/watch?v=tAGnKpE4NCI',
        'audio': 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3',
    },
    'Perfect': {
        'youtube': 'https://www.youtube.com/watch?v=2Vv-BfVoq4g',
        'audio': 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3',
    },
    'Riptide': {
        'youtube': 'https://www.youtube.com/watch?v=uJ_1HMAGb4k',
        'audio': 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-3.mp3',
    },
    'Shallow': {
        'youtube': 'https://www.youtube.com/watch?v=bo_efYhYU2A',
        'audio': 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-4.mp3',
    },
    'Someone Like You': {
        'youtube': 'https://www.youtube.com/watch?v=hLQl3WQQoQ0',
        'audio': 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-5.mp3',
    },
    'Stand By Me': {
        'youtube': 'https://www.youtube.com/watch?v=hwZNL7QVJjE',
        'audio': 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-6.mp3',
    },
    'Summertime': {
        'youtube': 'https://www.youtube.com/watch?v=MIDOEsQLWB8',
        'audio': 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-7.mp3',
    },
    'Sweet Home Alabama': {
        'youtube': 'https://www.youtube.com/watch?v=ye5BuYf8q4o',
        'audio': 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-8.mp3',
    },
    'Wish You Were Here': {
        'youtube': 'https://www.youtube.com/watch?v=IXdNnw99-Ic',
        'audio': 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-9.mp3',
    },
    'Wonderwall': {
        'youtube': 'https://www.youtube.com/watch?v=bx1Bh8ZvH84',
        'audio': 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3',
    },
    'Zombie': {
        'youtube': 'https://www.youtube.com/watch?v=6Ejga4kJUts',
        'audio': 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-10.mp3',
    },
}

class Command(BaseCommand):
    help = 'Populates all songs with YouTube and MP3 audio links'

    def handle(self, *args, **options):
        self.stdout.write("Attaching YouTube and MP3 links to ALL songs in the database...")
        updated = 0
        for tab in Tab.objects.all():
            media = SONG_MEDIA.get(tab.title)
            if media:
                tab.youtube_url = media['youtube']
                tab.audio_url = media['audio']
                tab.save()
                updated += 1
                self.stdout.write(f"  + Added media to: {tab.title}")
            else:
                # Default fallback demo links if title didn't match exactly
                tab.youtube_url = 'https://www.youtube.com/watch?v=bx1Bh8ZvH84'
                tab.audio_url = 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3'
                tab.save()
                updated += 1
                self.stdout.write(f"  + Added default media to: {tab.title}")

        self.stdout.write(self.style.SUCCESS(f"Successfully attached YouTube & MP3 links to all {updated} songs!"))
