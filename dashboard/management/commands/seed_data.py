from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from dashboard.models import UserProfile, Chord, Tab, PracticeSession, UserChordProgress
from django.utils import timezone
from datetime import timedelta
import random

# Complete guitar chord database covering all 12 musical keys and common variations
ALL_KEY_CHORDS = [
    # ================= 12 MAJOR CHORDS =================
    {
        'name': 'C Major',
        'genre': 'Acoustic',
        'difficulty': 'Easy',
        'diagram_data': {'frets': [-1, 3, 2, 0, 1, 0], 'fingers': [0, 3, 2, 0, 1, 0], 'base_fret': 1, 'barres': []}
    },
    {
        'name': 'C# Major',
        'genre': 'Rock',
        'difficulty': 'Hard',
        'diagram_data': {'frets': [-1, 4, 6, 6, 6, 4], 'fingers': [0, 1, 2, 3, 4, 1], 'base_fret': 4, 'barres': [4]}
    },
    {
        'name': 'Db Major',
        'genre': 'Pop',
        'difficulty': 'Hard',
        'diagram_data': {'frets': [-1, 4, 6, 6, 6, 4], 'fingers': [0, 1, 2, 3, 4, 1], 'base_fret': 4, 'barres': [4]}
    },
    {
        'name': 'D Major',
        'genre': 'Pop',
        'difficulty': 'Easy',
        'diagram_data': {'frets': [-1, -1, 0, 2, 3, 2], 'fingers': [0, 0, 0, 1, 3, 2], 'base_fret': 1, 'barres': []}
    },
    {
        'name': 'Eb Major',
        'genre': 'Jazz',
        'difficulty': 'Hard',
        'diagram_data': {'frets': [-1, 6, 8, 8, 8, 6], 'fingers': [0, 1, 2, 3, 4, 1], 'base_fret': 6, 'barres': [6]}
    },
    {
        'name': 'E Major',
        'genre': 'Rock',
        'difficulty': 'Easy',
        'diagram_data': {'frets': [0, 2, 2, 1, 0, 0], 'fingers': [0, 2, 3, 1, 0, 0], 'base_fret': 1, 'barres': []}
    },
    {
        'name': 'F Major',
        'genre': 'Rock',
        'difficulty': 'Medium',
        'diagram_data': {'frets': [1, 3, 3, 2, 1, 1], 'fingers': [1, 3, 4, 2, 1, 1], 'base_fret': 1, 'barres': [1]}
    },
    {
        'name': 'F# Major',
        'genre': 'Rock',
        'difficulty': 'Hard',
        'diagram_data': {'frets': [2, 4, 4, 3, 2, 2], 'fingers': [1, 3, 4, 2, 1, 1], 'base_fret': 2, 'barres': [2]}
    },
    {
        'name': 'Gb Major',
        'genre': 'Pop',
        'difficulty': 'Hard',
        'diagram_data': {'frets': [2, 4, 4, 3, 2, 2], 'fingers': [1, 3, 4, 2, 1, 1], 'base_fret': 2, 'barres': [2]}
    },
    {
        'name': 'G Major',
        'genre': 'Acoustic',
        'difficulty': 'Easy',
        'diagram_data': {'frets': [3, 2, 0, 0, 0, 3], 'fingers': [2, 1, 0, 0, 0, 3], 'base_fret': 1, 'barres': []}
    },
    {
        'name': 'Ab Major',
        'genre': 'Jazz',
        'difficulty': 'Hard',
        'diagram_data': {'frets': [4, 6, 6, 5, 4, 4], 'fingers': [1, 3, 4, 2, 1, 1], 'base_fret': 4, 'barres': [4]}
    },
    {
        'name': 'A Major',
        'genre': 'Pop',
        'difficulty': 'Easy',
        'diagram_data': {'frets': [-1, 0, 2, 2, 2, 0], 'fingers': [0, 0, 1, 2, 3, 0], 'base_fret': 1, 'barres': []}
    },
    {
        'name': 'Bb Major',
        'genre': 'Jazz',
        'difficulty': 'Medium',
        'diagram_data': {'frets': [-1, 1, 3, 3, 3, 1], 'fingers': [0, 1, 2, 3, 4, 1], 'base_fret': 1, 'barres': [1]}
    },
    {
        'name': 'B Major',
        'genre': 'Rock',
        'difficulty': 'Hard',
        'diagram_data': {'frets': [-1, 2, 4, 4, 4, 2], 'fingers': [0, 1, 2, 3, 4, 1], 'base_fret': 2, 'barres': [2]}
    },

    # ================= 12 MINOR CHORDS =================
    {
        'name': 'C Minor',
        'genre': 'Rock',
        'difficulty': 'Medium',
        'diagram_data': {'frets': [-1, 3, 5, 5, 4, 3], 'fingers': [0, 1, 3, 4, 2, 1], 'base_fret': 3, 'barres': [3]}
    },
    {
        'name': 'C# Minor',
        'genre': 'Rock',
        'difficulty': 'Hard',
        'diagram_data': {'frets': [-1, 4, 6, 6, 5, 4], 'fingers': [0, 1, 3, 4, 2, 1], 'base_fret': 4, 'barres': [4]}
    },
    {
        'name': 'D Minor',
        'genre': 'Acoustic',
        'difficulty': 'Easy',
        'diagram_data': {'frets': [-1, -1, 0, 2, 3, 1], 'fingers': [0, 0, 0, 2, 3, 1], 'base_fret': 1, 'barres': []}
    },
    {
        'name': 'D# Minor',
        'genre': 'Jazz',
        'difficulty': 'Hard',
        'diagram_data': {'frets': [-1, 6, 8, 8, 7, 6], 'fingers': [0, 1, 3, 4, 2, 1], 'base_fret': 6, 'barres': [6]}
    },
    {
        'name': 'Eb Minor',
        'genre': 'Jazz',
        'difficulty': 'Hard',
        'diagram_data': {'frets': [-1, 6, 8, 8, 7, 6], 'fingers': [0, 1, 3, 4, 2, 1], 'base_fret': 6, 'barres': [6]}
    },
    {
        'name': 'E Minor',
        'genre': 'Rock',
        'difficulty': 'Easy',
        'diagram_data': {'frets': [0, 2, 2, 0, 0, 0], 'fingers': [0, 2, 3, 0, 0, 0], 'base_fret': 1, 'barres': []}
    },
    {
        'name': 'F Minor',
        'genre': 'Rock',
        'difficulty': 'Hard',
        'diagram_data': {'frets': [1, 3, 3, 1, 1, 1], 'fingers': [1, 3, 4, 1, 1, 1], 'base_fret': 1, 'barres': [1]}
    },
    {
        'name': 'F# Minor',
        'genre': 'Pop',
        'difficulty': 'Hard',
        'diagram_data': {'frets': [2, 4, 4, 2, 2, 2], 'fingers': [1, 3, 4, 1, 1, 1], 'base_fret': 2, 'barres': [2]}
    },
    {
        'name': 'G Minor',
        'genre': 'Rock',
        'difficulty': 'Medium',
        'diagram_data': {'frets': [3, 5, 5, 3, 3, 3], 'fingers': [1, 3, 4, 1, 1, 1], 'base_fret': 3, 'barres': [3]}
    },
    {
        'name': 'G# Minor',
        'genre': 'Rock',
        'difficulty': 'Hard',
        'diagram_data': {'frets': [4, 6, 6, 4, 4, 4], 'fingers': [1, 3, 4, 1, 1, 1], 'base_fret': 4, 'barres': [4]}
    },
    {
        'name': 'A Minor',
        'genre': 'Acoustic',
        'difficulty': 'Easy',
        'diagram_data': {'frets': [-1, 0, 2, 2, 1, 0], 'fingers': [0, 0, 2, 3, 1, 0], 'base_fret': 1, 'barres': []}
    },
    {
        'name': 'A# Minor',
        'genre': 'Jazz',
        'difficulty': 'Hard',
        'diagram_data': {'frets': [-1, 1, 3, 3, 2, 1], 'fingers': [0, 1, 3, 4, 2, 1], 'base_fret': 1, 'barres': [1]}
    },
    {
        'name': 'Bb Minor',
        'genre': 'Jazz',
        'difficulty': 'Medium',
        'diagram_data': {'frets': [-1, 1, 3, 3, 2, 1], 'fingers': [0, 1, 3, 4, 2, 1], 'base_fret': 1, 'barres': [1]}
    },
    {
        'name': 'B Minor',
        'genre': 'Rock',
        'difficulty': 'Medium',
        'diagram_data': {'frets': [-1, 2, 4, 4, 3, 2], 'fingers': [0, 1, 3, 4, 2, 1], 'base_fret': 2, 'barres': [2]}
    },

    # ================= 12 DIMINISHED CHORDS =================
    {
        'name': 'C Diminished',
        'genre': 'Jazz',
        'difficulty': 'Medium',
        'diagram_data': {'frets': [-1, 3, 4, 5, 4, -1], 'fingers': [0, 1, 2, 4, 3, 0], 'base_fret': 2, 'barres': []}
    },
    {
        'name': 'C# Diminished',
        'genre': 'Jazz',
        'difficulty': 'Medium',
        'diagram_data': {'frets': [-1, -1, 2, 3, 2, 3], 'fingers': [0, 0, 1, 3, 2, 4], 'base_fret': 1, 'barres': []}
    },
    {
        'name': 'D Diminished',
        'genre': 'Jazz',
        'difficulty': 'Medium',
        'diagram_data': {'frets': [-1, -1, 0, 1, 3, 1], 'fingers': [0, 0, 0, 1, 3, 2], 'base_fret': 1, 'barres': []}
    },
    {
        'name': 'D# Diminished',
        'genre': 'Jazz',
        'difficulty': 'Hard',
        'diagram_data': {'frets': [-1, -1, 1, 2, 1, 2], 'fingers': [0, 0, 1, 3, 2, 4], 'base_fret': 1, 'barres': []}
    },
    {
        'name': 'E Diminished',
        'genre': 'Jazz',
        'difficulty': 'Medium',
        'diagram_data': {'frets': [-1, -1, 2, 3, 2, 3], 'fingers': [0, 0, 1, 3, 2, 4], 'base_fret': 1, 'barres': []}
    },
    {
        'name': 'F Diminished',
        'genre': 'Jazz',
        'difficulty': 'Hard',
        'diagram_data': {'frets': [-1, -1, 3, 4, 3, 4], 'fingers': [0, 0, 1, 3, 2, 4], 'base_fret': 2, 'barres': []}
    },
    {
        'name': 'F# Diminished',
        'genre': 'Jazz',
        'difficulty': 'Hard',
        'diagram_data': {'frets': [-1, -1, 4, 5, 4, 5], 'fingers': [0, 0, 1, 3, 2, 4], 'base_fret': 3, 'barres': []}
    },
    {
        'name': 'G Diminished',
        'genre': 'Jazz',
        'difficulty': 'Medium',
        'diagram_data': {'frets': [-1, -1, 5, 6, 5, 6], 'fingers': [0, 0, 1, 3, 2, 4], 'base_fret': 4, 'barres': []}
    },
    {
        'name': 'G# Diminished',
        'genre': 'Jazz',
        'difficulty': 'Hard',
        'diagram_data': {'frets': [-1, -1, 6, 7, 6, 7], 'fingers': [0, 0, 1, 3, 2, 4], 'base_fret': 5, 'barres': []}
    },
    {
        'name': 'A Diminished',
        'genre': 'Jazz',
        'difficulty': 'Medium',
        'diagram_data': {'frets': [-1, 0, 1, 2, 1, -1], 'fingers': [0, 0, 1, 3, 2, 0], 'base_fret': 1, 'barres': []}
    },
    {
        'name': 'A# Diminished',
        'genre': 'Jazz',
        'difficulty': 'Hard',
        'diagram_data': {'frets': [-1, 1, 2, 3, 2, -1], 'fingers': [0, 1, 2, 4, 3, 0], 'base_fret': 1, 'barres': []}
    },
    {
        'name': 'B Diminished',
        'genre': 'Jazz',
        'difficulty': 'Medium',
        'diagram_data': {'frets': [-1, 2, 3, 4, 3, -1], 'fingers': [0, 1, 2, 4, 3, 0], 'base_fret': 1, 'barres': []}
    },

    # ================= 7TH, SUS & EXTENDED CHORDS =================
    {
        'name': 'C7',
        'genre': 'Jazz',
        'difficulty': 'Medium',
        'diagram_data': {'frets': [-1, 3, 2, 3, 1, 0], 'fingers': [0, 3, 2, 4, 1, 0], 'base_fret': 1, 'barres': []}
    },
    {
        'name': 'A7',
        'genre': 'Jazz',
        'difficulty': 'Easy',
        'diagram_data': {'frets': [-1, 0, 2, 0, 2, 0], 'fingers': [0, 0, 1, 0, 2, 0], 'base_fret': 1, 'barres': []}
    },
    {
        'name': 'D7',
        'genre': 'Pop',
        'difficulty': 'Easy',
        'diagram_data': {'frets': [-1, -1, 0, 2, 1, 2], 'fingers': [0, 0, 0, 2, 1, 3], 'base_fret': 1, 'barres': []}
    },
    {
        'name': 'E7',
        'genre': 'Jazz',
        'difficulty': 'Easy',
        'diagram_data': {'frets': [0, 2, 0, 1, 0, 0], 'fingers': [0, 2, 0, 1, 0, 0], 'base_fret': 1, 'barres': []}
    },
    {
        'name': 'G7',
        'genre': 'Acoustic',
        'difficulty': 'Easy',
        'diagram_data': {'frets': [3, 2, 0, 0, 0, 1], 'fingers': [3, 2, 0, 0, 0, 1], 'base_fret': 1, 'barres': []}
    },
    {
        'name': 'B7',
        'genre': 'Acoustic',
        'difficulty': 'Medium',
        'diagram_data': {'frets': [-1, 2, 1, 2, 0, 2], 'fingers': [0, 2, 1, 3, 0, 4], 'base_fret': 1, 'barres': []}
    },
    {
        'name': 'Cmaj7',
        'genre': 'Jazz',
        'difficulty': 'Medium',
        'diagram_data': {'frets': [-1, 3, 2, 0, 0, 0], 'fingers': [0, 3, 2, 0, 0, 0], 'base_fret': 1, 'barres': []}
    },
    {
        'name': 'Fmaj7',
        'genre': 'Jazz',
        'difficulty': 'Medium',
        'diagram_data': {'frets': [-1, -1, 3, 2, 1, 0], 'fingers': [0, 0, 3, 2, 1, 0], 'base_fret': 1, 'barres': []}
    },
    {
        'name': 'Gmaj7',
        'genre': 'Jazz',
        'difficulty': 'Medium',
        'diagram_data': {'frets': [3, 2, 0, 0, 0, 2], 'fingers': [2, 1, 0, 0, 0, 3], 'base_fret': 1, 'barres': []}
    },
    {
        'name': 'Am7',
        'genre': 'Jazz',
        'difficulty': 'Easy',
        'diagram_data': {'frets': [-1, 0, 2, 0, 1, 0], 'fingers': [0, 0, 2, 0, 1, 0], 'base_fret': 1, 'barres': []}
    },
    {
        'name': 'Dm7',
        'genre': 'Jazz',
        'difficulty': 'Medium',
        'diagram_data': {'frets': [-1, -1, 0, 2, 1, 1], 'fingers': [0, 0, 0, 2, 1, 1], 'base_fret': 1, 'barres': [1]}
    },
    {
        'name': 'Em7',
        'genre': 'Rock',
        'difficulty': 'Easy',
        'diagram_data': {'frets': [0, 2, 0, 0, 0, 0], 'fingers': [0, 1, 0, 0, 0, 0], 'base_fret': 1, 'barres': []}
    },
    {
        'name': 'Dsus4',
        'genre': 'Pop',
        'difficulty': 'Easy',
        'diagram_data': {'frets': [-1, -1, 0, 2, 3, 3], 'fingers': [0, 0, 0, 1, 2, 4], 'base_fret': 1, 'barres': []}
    },
    {
        'name': 'Asus2',
        'genre': 'Rock',
        'difficulty': 'Easy',
        'diagram_data': {'frets': [-1, 0, 2, 2, 0, 0], 'fingers': [0, 0, 1, 2, 0, 0], 'base_fret': 1, 'barres': []}
    },
    {
        'name': 'Cadd9',
        'genre': 'Acoustic',
        'difficulty': 'Easy',
        'diagram_data': {'frets': [-1, 3, 2, 0, 3, 0], 'fingers': [0, 2, 1, 0, 3, 0], 'base_fret': 1, 'barres': []}
    },
    {
        'name': 'A7sus4',
        'genre': 'Acoustic',
        'difficulty': 'Easy',
        'diagram_data': {'frets': [-1, 0, 2, 0, 3, 0], 'fingers': [0, 0, 1, 0, 2, 0], 'base_fret': 1, 'barres': []}
    },
    {
        'name': 'E5',
        'genre': 'Rock',
        'difficulty': 'Easy',
        'diagram_data': {'frets': [0, 2, 2, -1, -1, -1], 'fingers': [0, 1, 2, 0, 0, 0], 'base_fret': 1, 'barres': []}
    },
    {
        'name': 'A5',
        'genre': 'Rock',
        'difficulty': 'Easy',
        'diagram_data': {'frets': [-1, 0, 2, 2, -1, -1], 'fingers': [0, 0, 1, 2, 0, 0], 'base_fret': 1, 'barres': []}
    },
]

# Comprehensive Song Catalog across Acoustic, Rock, Pop, and Jazz
SONGS_CATALOG = [
    # ---- ACOUSTIC CLASSICS ----
    {
        'title': 'Wonderwall',
        'artist': 'Oasis',
        'genre': 'Acoustic',
        'difficulty': 'Easy',
        'key': 'G',
        'chords': ['E Minor', 'G Major', 'D Major', 'A Major', 'C Major'],
        'content': """Capo: 2nd Fret | Strumming: D-D-D-D-DU (Down Down Down Down Up Down Up)

[Intro]
Em7 - G - Dsus4 - A7sus4 (x4)

[Verse 1]
Em7          G
Today is gonna be the day
                  Dsus4             A7sus4
That they're gonna throw it back to you
Em7               G
By now you should've somehow
        Dsus4               A7sus4
Realized what you gotta do
Em7                 G
I don't believe that anybody
Dsus4          A7sus4          Cadd9  Dsus4  A7sus4
Feels the way I do about you now

[Chorus]
Cadd9          Em7                 G
And all the roads that lead you there are winding
Cadd9          Em7                 G
And all the lights that light the way are blinding
Cadd9          Em7
There are many things that I would
G                 Em7
Like to say to you
                 A7sus4
But I don't know how

[Refrain]
Cadd9    Em7    G
Because maybe
            Em7               Cadd9   Em7   G
You're gonna be the one that saves me
    Em7     Cadd9   Em7   G
And after all
            Em7    Cadd9   Em7   G   Em7
You're my wonderwall"""
    },
    {
        'title': 'Knockin\' on Heaven\'s Door',
        'artist': 'Bob Dylan',
        'genre': 'Acoustic',
        'difficulty': 'Easy',
        'key': 'G',
        'chords': ['G Major', 'D Major', 'A Minor', 'C Major'],
        'content': """Capo: None | Strumming: D-D-UDU

[Verse 1]
G         D                Am
Mama, take this badge off of me
G         D          C
I can't use it anymore
G            D                  Am
It's gettin' dark, too dark for me to see
G            D                    C
I feel like I'm knockin' on heaven's door

[Chorus]
G            D                    Am
Knock, knock, knockin' on heaven's door
G            D                    C
Knock, knock, knockin' on heaven's door
G            D                    Am
Knock, knock, knockin' on heaven's door
G            D                    C
Knock, knock, knockin' on heaven's door

[Verse 2]
G         D                Am
Mama, put my guns in the ground
G         D          C
I can't shoot them anymore
G            D                  Am
That long black cloud is comin' down
G            D                    C
I feel like I'm knockin' on heaven's door"""
    },
    {
        'title': 'Horse with No Name',
        'artist': 'America',
        'genre': 'Acoustic',
        'difficulty': 'Easy',
        'key': 'E Minor',
        'chords': ['E Minor', 'D Major'],
        'content': """Capo: None | Strumming: D-DU-UDU (Two-Chord Masterpiece)

[Verse 1]
Em                      D
On the first part of the journey
Em                      D
I was looking at all the life
Em                           D
There were plants and birds and rocks and things
Em                    D
There was sand and hills and rings

[Chorus]
Em                                  D
I've been through the desert on a horse with no name
Em                           D
It felt good to be out of the rain
Em                       D
In the desert you can't remember your name
Em                                D
'Cause there ain't no one for to give you no pain
Em        D       Em        D
La la la, la-la-la, la la la, la la"""
    },
    {
        'title': 'Wish You Were Here',
        'artist': 'Pink Floyd',
        'genre': 'Rock',
        'difficulty': 'Easy',
        'key': 'G',
        'chords': ['G Major', 'C Major', 'D Major', 'A Minor', 'E Minor'],
        'content': """Capo: None | Strumming: D-D-U-U-D-U

[Intro]
Em7 - G - Em7 - G - Em7 - A7sus4 - Em7 - A7sus4 - G

[Verse]
C                               D
So, so you think you can tell
            Am
Heaven from hell?
                G
Blue skies from pain?
                     D
Can you tell a green field
                  C
From a cold steel rail?
               Am
A smile from a veil?
                     G
Do you think you can tell?

[Chorus]
C                               D
How I wish, how I wish you were here
       Am                                       G
We're just two lost souls swimming in a fish bowl, year after year
D                                    C
Running over the same old ground, and what have we found?
             Am                      G
The same old fears, wish you were here"""
    },
    {
        'title': 'Hallelujah',
        'artist': 'Leonard Cohen',
        'genre': 'Acoustic',
        'difficulty': 'Easy',
        'key': 'C',
        'chords': ['C Major', 'A Minor', 'F Major', 'G Major', 'E Minor'],
        'content': """Capo: None (or Capo 5 for Jeff Buckley style) | 6/8 Time: D-D-D-D-D-D

[Verse 1]
    C                Am
Now I've heard there was a secret chord
     C                   Am
That David played, and it pleased the Lord
    F                G                C       G
But you don't really care for music, do you?
   C                   F           G
It goes like this, the fourth, the fifth
    Am              F
The minor fall, the major lift
    G                E7          Am
The baffled king composing Hallelujah

[Chorus]
       F           Am          F           C    G   C
Hallelujah, Hallelujah, Hallelujah, Hallelu-u-u-u-jah"""
    },
    {
        'title': 'Let It Be',
        'artist': 'The Beatles',
        'genre': 'Pop',
        'difficulty': 'Easy',
        'key': 'C',
        'chords': ['C Major', 'G Major', 'A Minor', 'F Major'],
        'content': """Capo: None | Strumming: D-D-D-D

[Verse 1]
C                G
When I find myself in times of trouble
Am           F
Mother Mary comes to me
C                 G              F      C
Speaking words of wisdom, let it be

C                G
And in my hour of darkness
       Am             F
She is standing right in front of me
C                 G              F      C
Speaking words of wisdom, let it be

[Chorus]
       Am         G          F          C
Let it be, let it be, let it be, let it be
C                G              F      C
Whisper words of wisdom, let it be"""
    },
    {
        'title': 'Stand By Me',
        'artist': 'Ben E. King',
        'genre': 'Pop',
        'difficulty': 'Easy',
        'key': 'G',
        'chords': ['G Major', 'E Minor', 'C Major', 'D Major'],
        'content': """Capo: 2nd Fret | Strumming: Bass-Strum-Slap-Strum

[Verse 1]
G
When the night has come
Em
And the land is dark
        C          D                 G
And the moon is the only light we'll see
      G
No, I won't be afraid, no, I won't be afraid
        Em
Just as long as you stand
      C     D         G
Stand by me, so darlin', darlin'

[Chorus]
G
Stand by me, oh, stand by me
     Em
Oh, stand, stand by me
C     D      G
Stand by me, stand by me"""
    },
    {
        'title': 'Blowin\' in the Wind',
        'artist': 'Bob Dylan',
        'genre': 'Acoustic',
        'difficulty': 'Easy',
        'key': 'G',
        'chords': ['G Major', 'C Major', 'D Major'],
        'content': """Capo: 7th Fret (Optional) | Strumming: D-DU-UDU

[Verse 1]
    G            C             G
How many roads must a man walk down
       G           C           D
Before you call him a man?
    G            C             G
How many seas must a white dove sail
       G           C           D
Before she sleeps in the sand?

[Chorus]
    C           D            G             Em
The answer, my friend, is blowin' in the wind
    C           D            G
The answer is blowin' in the wind"""
    },
    {
        'title': 'Fast Car',
        'artist': 'Tracy Chapman',
        'genre': 'Acoustic',
        'difficulty': 'Medium',
        'key': 'C',
        'chords': ['C Major', 'G Major', 'E Minor', 'D Major'],
        'content': """Capo: 2nd Fret | Fingerpicking: C - G - Em - D

[Verse 1]
C              G
You got a fast car
Em                    D
I want a ticket to anywhere
C                  G
Maybe we make a deal
Em                 D
Maybe together we can get somewhere
C                  G
Any place is better
Em                       D
Starting from zero got nothing to lose
C                   G
Maybe we'll make something
Em             D
Me, myself, I got nothing to prove

[Chorus]
      C
And I had a feeling that I belonged
Em
I had a feeling I could be someone
D
Be someone, be someone"""
    },
    {
        'title': 'Hey There Delilah',
        'artist': 'Plain White T\'s',
        'genre': 'Acoustic',
        'difficulty': 'Easy',
        'key': 'D',
        'chords': ['D Major', 'F# Minor', 'B Minor', 'G Major', 'A Major'],
        'content': """Capo: None | Fingerstyle / Strumming: Pluck-Strum

[Verse 1]
D                           F#m
Hey there, Delilah, what's it like in New York City?
        D                                     F#m
I'm a thousand miles away, but girl, tonight you look so pretty
        Bm     G                   A                Bm
Yes you do, Times Square can't shine as bright as you
          A
I swear it's true

[Chorus]
D                 Bm
Oh, it's what you do to me
D                 Bm
Oh, it's what you do to me
D                 Bm
Oh, it's what you do to me
D                 Bm
What you do to me"""
    },

    # ---- ROCK CLASSICS ----
    {
        'title': 'Hotel California',
        'artist': 'Eagles',
        'genre': 'Rock',
        'difficulty': 'Medium',
        'key': 'B Minor',
        'chords': ['B Minor', 'F# Major', 'A Major', 'E Major', 'G Major', 'D Major', 'E Minor'],
        'content': """Capo: 7th Fret (for acoustic 12-string) or Open Bm | 4/4 Time

[Intro]
Bm - F# - A - E - G - D - Em - F#

[Verse 1]
Bm                          F#
On a dark desert highway, cool wind in my hair
A                         E
Warm smell of colitas, rising up through the air
G                          D
Up ahead in the distance, I saw a shimmering light
Em
My head grew heavy and my sight grew dim
F#
I had to stop for the night

[Chorus]
G                        D
Welcome to the Hotel California
        F#                                Bm
Such a lovely place (such a lovely place), such a lovely face
G                               D
Plenty of room at the Hotel California
     Em                             F#
Any time of year (any time of year), you can find it here"""
    },
    {
        'title': 'Sweet Home Alabama',
        'artist': 'Lynyrd Skynyrd',
        'genre': 'Rock',
        'difficulty': 'Easy',
        'key': 'D',
        'chords': ['D Major', 'C Major', 'G Major'],
        'content': """Capo: None | Main Riff: D - C - G

[Verse 1]
D       C           G
Big wheels keep on turnin'
D       C               G
Carry me home to see my kin
D       C              G
Singin' songs about the south-land
D       C            G
I miss 'ole 'Bama once again, and I think it's a sin, yes

[Chorus]
D     C        G
Sweet home Alabama
D       C              G
Where the skies are so blue
D     C        G
Sweet home Alabama
D        C                 G
Lord, I'm comin' home to you"""
    },
    {
        'title': 'Zombie',
        'artist': 'The Cranberries',
        'genre': 'Rock',
        'difficulty': 'Easy',
        'key': 'E Minor',
        'chords': ['E Minor', 'C Major', 'G Major', 'D Major'],
        'content': """Capo: None | Strumming: Powerful Down-Strums: Em - C - G - D

[Verse 1]
Em               C
Another head hangs lowly
G                D
Child is slowly taken
Em                      C
And the violence caused such silence
G               D
Who are we mistaken?

[Chorus]
             Em
In your head, in your head
         C
Zombie, zombie, zombie-ie-ie
             G
What's in your head, in your head
         D
Zombie, zombie, zombie-ie-ie-ie, oh"""
    },
    {
        'title': 'Creep',
        'artist': 'Radiohead',
        'genre': 'Rock',
        'difficulty': 'Medium',
        'key': 'G',
        'chords': ['G Major', 'B Major', 'C Major', 'C Minor'],
        'content': """Capo: None | Progression: G - B - C - Cm (Arpeggiated)

[Verse 1]
G
When you were here before
B
Couldn't look you in the eye
C
You're just like an angel
Cm
Your skin makes me cry

[Chorus]
               G
But I'm a creep
          B
I'm a weirdo
                          C
What the hell am I doin' here?
                Cm
I don't belong here"""
    },
    {
        'title': 'Nothing Else Matters',
        'artist': 'Metallica',
        'genre': 'Rock',
        'difficulty': 'Medium',
        'key': 'E Minor',
        'chords': ['E Minor', 'D Major', 'C Major', 'G Major', 'B7'],
        'content': """Capo: None | 6/8 Time Fingerpicking: E-G-B-e-B-G

[Verse 1]
Em                     D         C
So close, no matter how far
Em                        D         C
Couldn't be much more from the heart
Em                     D         C
Forever trusting who we are
G        B7        Em
And nothing else matters

[Chorus]
C   A   D
Never cared for what they do
C   A   D
Never cared for what they know
C   A   D        Em
And I know"""
    },
    {
        'title': 'Bad Moon Rising',
        'artist': 'Creedence Clearwater Revival',
        'genre': 'Rock',
        'difficulty': 'Easy',
        'key': 'D',
        'chords': ['D Major', 'A Major', 'G Major'],
        'content': """Capo: None | Strumming: D-D-U-U-D-U

[Verse 1]
D       A     G    D
I see the bad moon a-risin'
D       A       G       D
I see trouble on the way
D       A       G       D
I see earthquakes and lightnin'
D       A     G     D
I see bad times today

[Chorus]
G
Don't go 'round tonight
          D
Well it's bound to take your life
A             G                  D
There's a bad moon on the rise"""
    },
    {
        'title': 'Californication',
        'artist': 'Red Hot Chili Peppers',
        'genre': 'Rock',
        'difficulty': 'Medium',
        'key': 'A Minor',
        'chords': ['A Minor', 'F Major', 'C Major', 'G Major', 'D Minor'],
        'content': """Capo: None | Riff: Am - F

[Verse 1]
Am                             F
Psychic spies from China try to steal your mind's elation
Am                                  F
And little girls from Sweden dream of silver screen quotation
C              G       F            Dm
And if you want these kind of dreams it's Californication

[Chorus]
Am                   F
Destruction leads to a very rough road
     Am                     F
But it also breeds creation
C              G       F            Dm
And earthquakes are to a girl's guitar, they're just another good vibration
C              G       Dm
And tidal waves couldn't save the world from Californication"""
    },

    # ---- POP & CONTEMPORARY ----
    {
        'title': 'Riptide',
        'artist': 'Vance Joy',
        'genre': 'Pop',
        'difficulty': 'Easy',
        'key': 'C',
        'chords': ['A Minor', 'G Major', 'C Major', 'F Major'],
        'content': """Capo: 1st Fret | Strumming: D-D-U-D-U (Am - G - C)

[Verse 1]
Am         G                    C
I was scared of dentists and the dark
Am         G                C
I was scared of pretty girls and starting conversations
Am         G                  C
Oh, all my friends are turning green
Am                 G                C
You're the magician's assistant in their dream

[Chorus]
Am      G               C
Lady, running down to the riptide
          C
Taken away to the dark side
Am       G           C
I wanna be your left-hand man
Am        G                  C
I love you when you're singing that song
           C
And I got a lump in my throat
         Am           G              C
'Cause you're gonna sing the words wrong"""
    },
    {
        'title': 'Counting Stars',
        'artist': 'OneRepublic',
        'genre': 'Pop',
        'difficulty': 'Medium',
        'key': 'A Minor',
        'chords': ['A Minor', 'C Major', 'G Major', 'F Major'],
        'content': """Capo: 4th Fret | Progression: Am - C - G - F

[Chorus]
Am
Lately, I've been, I've been losing sleep
C
Dreaming about the things that we could be
G
But baby, I've been, I've been praying hard
F
Said, no more counting dollars, we'll be counting stars

[Verse 1]
Am
I see this life like a swinging vine
C
Swing my heart across the line
G
In my face is flashing signs
F
Seek it out and ye shall find"""
    },
    {
        'title': 'Someone Like You',
        'artist': 'Adele',
        'genre': 'Pop',
        'difficulty': 'Easy',
        'key': 'A',
        'chords': ['A Major', 'E Major', 'F# Minor', 'D Major'],
        'content': """Capo: 2nd Fret (G - D - Em - C) or Open (A - E - F#m - D)

[Verse 1]
A               E
I heard that you're settled down
         F#m
That you found a girl and you're
D
Married now
A               E
I heard that your dreams came true
           F#m
Guess she gave you things I didn't
D
Give to you

[Chorus]
A               E            F#m    D
Never mind, I'll find someone like you
         A            E          F#m    D
I wish nothing but the best for you, too
       A          E        F#m          D
"Don't forget me, I beg, I remember you said
             A                   E             F#m   D
Sometimes it lasts in love, but sometimes it hurts instead" """
    },
    {
        'title': 'I\'m Yours',
        'artist': 'Jason Mraz',
        'genre': 'Pop',
        'difficulty': 'Easy',
        'key': 'G',
        'chords': ['G Major', 'D Major', 'E Minor', 'C Major'],
        'content': """Capo: 4th Fret | Reggae Strumming: Down-Chop (Off-beat accent)

[Verse 1]
G
Well, you done done me, and you bet I felt it
D
I tried to be chill, but you're so hot that I melted
Em
I fell right through the cracks
             C
Now I'm tryin' to get back

[Chorus]
             G            D
So I won't hesitate no more, no more
       Em        C
It cannot wait, I'm yours"""
    },
    {
        'title': 'Perfect',
        'artist': 'Ed Sheeran',
        'genre': 'Pop',
        'difficulty': 'Easy',
        'key': 'G',
        'chords': ['G Major', 'E Minor', 'C Major', 'D Major'],
        'content': """Capo: 1st Fret | 6/8 Ballad Time: G - Em - C - D

[Verse 1]
G
I found a love for me
Em
Darling, just dive right in and follow my lead
G
Well, I found a girl, beautiful and sweet
Em                                    C                    D
Oh, I never knew you were the someone waiting for me

[Chorus]
        G                     Em
Baby, I'm dancing in the dark
                C
With you between my arms
              G
Barefoot on the grass
              Em
Listening to our favorite song
         C                         D                 G
When you said you looked a mess, I whispered underneath my breath
          D                   G
"You look perfect tonight" """
    },
    {
        'title': 'Shallow',
        'artist': 'Lady Gaga & Bradley Cooper',
        'genre': 'Pop',
        'difficulty': 'Easy',
        'key': 'G',
        'chords': ['E Minor', 'D Major', 'G Major', 'C Major', 'A Minor'],
        'content': """Capo: None | Fingerstyle Intro: Em - D/F# - G - C

[Verse 1]
Em       D/F#   G
Tell me somethin', girl
C                       G      D
Are you happy in this modern world?
Em       D/F#   G
Or do you need more?
C                             G          D
Is there somethin' else you're searchin' for?

[Chorus]
Am                         D
I'm off the deep end, watch as I dive in
G           D        Em
I'll never meet the ground
Am                             D
Crash through the surface where they can't hurt us
      G          D            Em
We're far from the shallow now"""
    },

    # ---- JAZZ & BLUES ----
    {
        'title': 'Fly Me to the Moon',
        'artist': 'Frank Sinatra',
        'genre': 'Jazz',
        'difficulty': 'Medium',
        'key': 'C',
        'chords': ['A Minor', 'D Minor', 'G7', 'C Major', 'C7', 'Fmaj7', 'B7', 'E7'],
        'content': """Capo: None | Jazz Swing 4/4 Time

[Verse 1]
Am7          Dm7
Fly me to the moon
            G7          Cmaj7   C7
Let me play among the stars
Fmaj7           Dm7
Let me see what spring is like on
E7          Am7    A7
Jupiter and Mars

[Chorus]
Dm7          G7         Cmaj7   Am7
In other words, hold my hand
Dm7          G7         E7      Am7
In other words, baby, kiss me

[Verse 2]
Am7              Dm7
Fill my heart with song
            G7          Cmaj7   C7
And let me sing forever more
Fmaj7           Dm7
You are all I long for
        E7          Am7
All I worship and adore
Dm7          G7         Cmaj7   Am7
In other words, please be true
Dm7          G7         C
In other words, I love you"""
    },
    {
        'title': 'Autumn Leaves',
        'artist': 'Jazz Standard',
        'genre': 'Jazz',
        'difficulty': 'Medium',
        'key': 'E Minor',
        'chords': ['A Minor', 'D7', 'G Major', 'C Major', 'B7', 'E Minor'],
        'content': """Capo: None | Jazz Ballad Standard: ii - V - I - IV - vii° - III - vi

[Section A]
Am7          D7
The falling leaves
            Gmaj7       Cmaj7
Drift by the window
F#dim        B7
The autumn leaves
            Em
Of red and gold

[Section B]
Am7          D7
I see your lips
            Gmaj7       Cmaj7
The summer kisses
F#dim        B7
The sunburned hands
            Em
I used to hold

[Section C]
            B7                  Em
Since you went away the days grow long
            D7                  Gmaj7
And soon I'll hear old winter's song
        Cmaj7       B7          Em
But I miss you most of all, my darling
            F#dim       B7      Em
When autumn leaves start to fall"""
    },
    {
        'title': 'Summertime',
        'artist': 'George Gershwin',
        'genre': 'Jazz',
        'difficulty': 'Medium',
        'key': 'A Minor',
        'chords': ['A Minor', 'E7', 'C Major', 'D Major'],
        'content': """Capo: None | Blues / Jazz Lullaby: Am - E7

[Verse 1]
Am          E7        Am    E7
Summertime, and the livin' is easy
Dm                                 E7
Fish are jumpin' and the cotton is high
Am             E7          Am         E7
Oh, your daddy's rich and your ma is good-lookin'
C              Am     D7    E7      Am
So hush, little baby, don't you cry

[Verse 2]
Am                E7             Am        E7
One of these mornings you're gonna rise up singin'
Dm                                            E7
Then you'll spread your wings and you'll take to the sky
Am          E7             Am         E7
But till that morning, there's a-nothin' can harm you
C              Am     D7    E7      Am
With daddy and mammy standin' by"""
    },
]

class Command(BaseCommand):
    help = 'Seeds database with chords, comprehensive 25+ song library with lyrics/tabs, and sample user data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding database with chords and expanded song library...')

        # 1. Clean up old dummy chords
        Chord.objects.filter(name__startswith='Chord_').delete()

        # 2. Seed All Key Chords
        chord_instances = {}
        for cdata in ALL_KEY_CHORDS:
            chord, _ = Chord.objects.update_or_create(
                name=cdata['name'],
                defaults={
                    'genre': cdata['genre'],
                    'difficulty': cdata['difficulty'],
                    'diagram_data': cdata['diagram_data']
                }
            )
            chord_instances[cdata['name']] = chord

        self.stdout.write(self.style.SUCCESS(f'Successfully verified {len(chord_instances)} chords across all keys.'))

        # 3. Create or get demo user
        user, user_created = User.objects.get_or_create(username='demo_user')
        if user_created:
            user.set_password('password')
            user.save()
            UserProfile.objects.create(user=user, skill_level='Intermediate', weekly_goal_minutes=150)

        # 4. Seed User Progress for Chords
        for i, (name, chord) in enumerate(chord_instances.items()):
            status = 'Mastered' if chord.difficulty == 'Easy' and i < 8 else 'Learning'
            UserChordProgress.objects.update_or_create(
                user=user,
                chord=chord,
                defaults={'status': status}
            )

        # 5. Clean up old dummy tabs
        Tab.objects.filter(title__startswith='Tab_').delete()

        # 6. Seed All Songs from SONGS_CATALOG
        created_songs = 0
        for sdata in SONGS_CATALOG:
            tab, created = Tab.objects.update_or_create(
                title=sdata['title'],
                artist=sdata['artist'],
                defaults={
                    'genre': sdata['genre'],
                    'difficulty': sdata['difficulty'],
                    'key': sdata['key'],
                    'content': sdata['content'].strip()
                }
            )
            # Associate real chord instances
            assoc_chords = [chord_instances[c] for c in sdata['chords'] if c in chord_instances]
            tab.associated_chords.set(assoc_chords)
            created_songs += 1

        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {created_songs} authentic songs in the Song Library!'))
