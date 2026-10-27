from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import login, get_user_model
from django.contrib.auth.decorators import login_required
from django.utils.crypto import get_random_string
from django.views.decorators.http import require_POST
from .forms import RegistrationForm
from .forms_session import PracticeSessionForm
from .forms_song import SongForm
from .models import PracticeSession, Chord, Tab, UserChordProgress
from django.db.models import Sum, Count, Q
from datetime import date, timedelta

User = get_user_model()

def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'landing.html')

@require_POST
def guest_login(request):
    username = f'guest_{get_random_string(8)}'
    user = User.objects.create_user(username=username)
    user.set_unusable_password()
    user.save()
    login(request, user)
    return redirect('dashboard')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required
def logger(request):
    if request.method == 'POST':
        form = PracticeSessionForm(request.POST)
        if form.is_valid():
            session = form.save(commit=False)
            session.user = request.user
            session.save()
            return JsonResponse({
                'status': 'success',
                'session': {
                    'date': session.date.strftime('%b %d, %Y') if session.date else 'Today',
                    'duration_minutes': session.duration_minutes,
                    'focus_area': session.focus_area,
                    'notes': session.notes or ''
                }
            }, status=201)
        return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)

    form = PracticeSessionForm()
    recent_sessions = PracticeSession.objects.filter(user=request.user).order_by('-id')[:10]
    return render(request, 'logger.html', {'form': form, 'recent_sessions': recent_sessions})

KEY_DEFINITIONS = {
    'C': [
        (1, 'I', 'Tonic', 'C Major'),
        (2, 'ii', 'Supertonic', 'D Minor'),
        (3, 'iii', 'Mediant', 'E Minor'),
        (4, 'IV', 'Subdominant', 'F Major'),
        (5, 'V', 'Dominant', 'G Major'),
        (6, 'vi', 'Submediant', 'A Minor'),
        (7, 'vii°', 'Leading Tone', 'B Diminished'),
    ],
    'G': [
        (1, 'I', 'Tonic', 'G Major'),
        (2, 'ii', 'Supertonic', 'A Minor'),
        (3, 'iii', 'Mediant', 'B Minor'),
        (4, 'IV', 'Subdominant', 'C Major'),
        (5, 'V', 'Dominant', 'D Major'),
        (6, 'vi', 'Submediant', 'E Minor'),
        (7, 'vii°', 'Leading Tone', 'F# Diminished'),
    ],
    'D': [
        (1, 'I', 'Tonic', 'D Major'),
        (2, 'ii', 'Supertonic', 'E Minor'),
        (3, 'iii', 'Mediant', 'F# Minor'),
        (4, 'IV', 'Subdominant', 'G Major'),
        (5, 'V', 'Dominant', 'A Major'),
        (6, 'vi', 'Submediant', 'B Minor'),
        (7, 'vii°', 'Leading Tone', 'C# Diminished'),
    ],
    'A': [
        (1, 'I', 'Tonic', 'A Major'),
        (2, 'ii', 'Supertonic', 'B Minor'),
        (3, 'iii', 'Mediant', 'C# Minor'),
        (4, 'IV', 'Subdominant', 'D Major'),
        (5, 'V', 'Dominant', 'E Major'),
        (6, 'vi', 'Submediant', 'F# Minor'),
        (7, 'vii°', 'Leading Tone', 'G# Diminished'),
    ],
    'E': [
        (1, 'I', 'Tonic', 'E Major'),
        (2, 'ii', 'Supertonic', 'F# Minor'),
        (3, 'iii', 'Mediant', 'G# Minor'),
        (4, 'IV', 'Subdominant', 'A Major'),
        (5, 'V', 'Dominant', 'B Major'),
        (6, 'vi', 'Submediant', 'C# Minor'),
        (7, 'vii°', 'Leading Tone', 'D# Diminished'),
    ],
    'B': [
        (1, 'I', 'Tonic', 'B Major'),
        (2, 'ii', 'Supertonic', 'C# Minor'),
        (3, 'iii', 'Mediant', 'D# Minor'),
        (4, 'IV', 'Subdominant', 'E Major'),
        (5, 'V', 'Dominant', 'F# Major'),
        (6, 'vi', 'Submediant', 'G# Minor'),
        (7, 'vii°', 'Leading Tone', 'A# Diminished'),
    ],
    'F': [
        (1, 'I', 'Tonic', 'F Major'),
        (2, 'ii', 'Supertonic', 'G Minor'),
        (3, 'iii', 'Mediant', 'A Minor'),
        (4, 'IV', 'Subdominant', 'Bb Major'),
        (5, 'V', 'Dominant', 'C Major'),
        (6, 'vi', 'Submediant', 'D Minor'),
        (7, 'vii°', 'Leading Tone', 'E Diminished'),
    ],
    'Bb': [
        (1, 'I', 'Tonic', 'Bb Major'),
        (2, 'ii', 'Supertonic', 'C Minor'),
        (3, 'iii', 'Mediant', 'D Minor'),
        (4, 'IV', 'Subdominant', 'Eb Major'),
        (5, 'V', 'Dominant', 'F Major'),
        (6, 'vi', 'Submediant', 'G Minor'),
        (7, 'vii°', 'Leading Tone', 'A Diminished'),
    ],
    'Eb': [
        (1, 'I', 'Tonic', 'Eb Major'),
        (2, 'ii', 'Supertonic', 'F Minor'),
        (3, 'iii', 'Mediant', 'G Minor'),
        (4, 'IV', 'Subdominant', 'Ab Major'),
        (5, 'V', 'Dominant', 'Bb Major'),
        (6, 'vi', 'Submediant', 'C Minor'),
        (7, 'vii°', 'Leading Tone', 'D Diminished'),
    ],
    'Ab': [
        (1, 'I', 'Tonic', 'Ab Major'),
        (2, 'ii', 'Supertonic', 'Bb Minor'),
        (3, 'iii', 'Mediant', 'C Minor'),
        (4, 'IV', 'Subdominant', 'Db Major'),
        (5, 'V', 'Dominant', 'Eb Major'),
        (6, 'vi', 'Submediant', 'F Minor'),
        (7, 'vii°', 'Leading Tone', 'G Diminished'),
    ],
    'Db': [
        (1, 'I', 'Tonic', 'Db Major'),
        (2, 'ii', 'Supertonic', 'Eb Minor'),
        (3, 'iii', 'Mediant', 'F Minor'),
        (4, 'IV', 'Subdominant', 'Gb Major'),
        (5, 'V', 'Dominant', 'Ab Major'),
        (6, 'vi', 'Submediant', 'Bb Minor'),
        (7, 'vii°', 'Leading Tone', 'C Diminished'),
    ],
    'F#': [
        (1, 'I', 'Tonic', 'F# Major'),
        (2, 'ii', 'Supertonic', 'G# Minor'),
        (3, 'iii', 'Mediant', 'A# Minor'),
        (4, 'IV', 'Subdominant', 'B Major'),
        (5, 'V', 'Dominant', 'C# Major'),
        (6, 'vi', 'Submediant', 'D# Minor'),
        (7, 'vii°', 'Leading Tone', 'F Diminished'),
    ]
}

@login_required
def library(request):
    all_chords = Chord.objects.all().order_by('name')
    tabs = Tab.objects.all().prefetch_related('associated_chords')

    genre = request.GET.get('genre')
    difficulty = request.GET.get('difficulty')

    chords = all_chords
    if genre:
        chords = chords.filter(genre=genre)
        tabs = tabs.filter(genre=genre)
    if difficulty:
        chords = chords.filter(difficulty=difficulty)

    user_progress = UserChordProgress.objects.filter(user=request.user)
    mastered_ids = set(user_progress.filter(status='Mastered').values_list('chord_id', flat=True))
    learning_ids = set(user_progress.filter(status='Learning').values_list('chord_id', flat=True))

    all_chords_dict = {c.name: c for c in all_chords}
    available_keys = list(KEY_DEFINITIONS.keys())
    selected_key = request.GET.get('key', 'C')
    if selected_key not in KEY_DEFINITIONS:
        selected_key = 'C'

    key_chords = []
    for degree, roman, function_name, chord_name in KEY_DEFINITIONS[selected_key]:
        chord_obj = all_chords_dict.get(chord_name)
        key_chords.append({
            'degree': degree,
            'roman': roman,
            'function': function_name,
            'name': chord_name,
            'chord': chord_obj,
        })

    # Progressions for the selected key
    deg_map = {item['degree']: item['name'] for item in key_chords}
    common_progressions = [
        {'name': 'Pop / Rock Hit', 'formula': '1 - 5 - 6 - 4', 'chords': [deg_map.get(1), deg_map.get(5), deg_map.get(6), deg_map.get(4)]},
        {'name': 'Classic Blues / Rock', 'formula': '1 - 4 - 5', 'chords': [deg_map.get(1), deg_map.get(4), deg_map.get(5)]},
        {'name': 'Jazz & Pop Cadence', 'formula': '2 - 5 - 1', 'chords': [deg_map.get(2), deg_map.get(5), deg_map.get(1)]},
        {'name': 'Doo-Wop 50s Ballad', 'formula': '1 - 6 - 4 - 5', 'chords': [deg_map.get(1), deg_map.get(6), deg_map.get(4), deg_map.get(5)]},
    ]

    return render(request, 'library.html', {
        'chords': chords,
        'tabs': tabs,
        'user_progress': user_progress,
        'mastered_ids': mastered_ids,
        'learning_ids': learning_ids,
        'selected_genre': genre or '',
        'selected_difficulty': difficulty or '',
        'available_keys': available_keys,
        'selected_key': selected_key,
        'key_chords': key_chords,
        'common_progressions': common_progressions,
    })

@login_required
def songs(request):
    if request.method == 'POST':
        form = SongForm(request.POST)
        if form.is_valid():
            new_song = form.save()
            messages.success(request, f'"{new_song.title}" by {new_song.artist} has been added to your Song Library!')
            return redirect('songs')
        else:
            messages.error(request, 'Could not add song. Please check the form errors below.')
    else:
        form = SongForm()

    song_list = Tab.objects.all().prefetch_related('associated_chords').order_by('title')

    q = request.GET.get('q', '').strip()
    genre = request.GET.get('genre', '').strip()
    difficulty = request.GET.get('difficulty', '').strip()
    key = request.GET.get('key', '').strip()

    if q:
        song_list = song_list.filter(Q(title__icontains=q) | Q(artist__icontains=q) | Q(content__icontains=q))
    if genre:
        song_list = song_list.filter(genre=genre)
    if difficulty:
        song_list = song_list.filter(difficulty=difficulty)
    if key:
        song_list = song_list.filter(key=key)

    available_keys = sorted(list(set(Tab.objects.values_list('key', flat=True).distinct())))
    all_chords = Chord.objects.all().order_by('name')

    return render(request, 'songs.html', {
        'songs': song_list,
        'form': form,
        'all_chords': all_chords,
        'search_query': q,
        'selected_genre': genre,
        'selected_difficulty': difficulty,
        'selected_key': key,
        'available_keys': available_keys,
        'total_songs': Tab.objects.count(),
    })

@login_required
def tools(request):
    return render(request, 'tools.html')

@login_required
def settings(request):
    # Simplified settings view for now
    return render(request, 'settings.html')
