from django.http import JsonResponse
from .forms import RegistrationForm
from .forms_session import PracticeSessionForm
from .models import PracticeSession, Chord, Tab, UserChordProgress
from django.db.models import Sum, Count, Q
from datetime import date, timedelta

# ... (rest of imports)

@login_required
def logger(request):
    if request.method == 'POST':
        form = PracticeSessionForm(request.POST)
        if form.is_valid():
            session = form.save(commit=False)
            session.user = request.user
            session.save()
            return JsonResponse({'status': 'success'}, status=201)
        return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)

    form = PracticeSessionForm()
    return render(request, 'logger.html', {'form': form})

@login_required
def library(request):
    chords = Chord.objects.all()
    tabs = Tab.objects.all()

    genre = request.GET.get('genre')
    difficulty = request.GET.get('difficulty')

    if genre:
        chords = chords.filter(genre=genre)
        tabs = tabs.filter(genre=genre)
    if difficulty:
        chords = chords.filter(difficulty=difficulty)

    return render(request, 'library.html', {
        'chords': chords,
        'tabs': tabs,
        'user_progress': UserChordProgress.objects.filter(user=request.user)
    })

@login_required
def tools(request):
    return render(request, 'tools.html')

@login_required
def settings(request):
    # Simplified settings view for now
    return render(request, 'settings.html')
