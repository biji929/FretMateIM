from django import forms
from .models import Tab, Chord

class SongForm(forms.ModelForm):
    class Meta:
        model = Tab
        fields = ['title', 'artist', 'genre', 'difficulty', 'key', 'associated_chords', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full bg-white dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-xl px-4 py-2.5 text-gray-900 dark:text-gray-100 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm transition',
                'placeholder': 'e.g. Wonderwall',
                'required': True,
                'id': 'songTitleInput'
            }),
            'artist': forms.TextInput(attrs={
                'class': 'w-full bg-white dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-xl px-4 py-2.5 text-gray-900 dark:text-gray-100 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm transition',
                'placeholder': 'e.g. Oasis',
                'required': True,
                'id': 'songArtistInput'
            }),
            'genre': forms.Select(attrs={
                'class': 'w-full bg-white dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-xl px-4 py-2.5 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm cursor-pointer transition',
                'id': 'songGenreInput'
            }),
            'difficulty': forms.Select(attrs={
                'class': 'w-full bg-white dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-xl px-4 py-2.5 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm cursor-pointer transition',
                'id': 'songDifficultyInput'
            }),
            'key': forms.TextInput(attrs={
                'class': 'w-full bg-white dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-xl px-4 py-2.5 text-gray-900 dark:text-gray-100 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm transition',
                'placeholder': 'e.g. G, C, or Em',
                'id': 'songKeyInput'
            }),
            'associated_chords': forms.SelectMultiple(attrs={
                'class': 'w-full bg-white dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-xl p-3 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm h-36 transition',
                'id': 'songChordsInput'
            }),
            'content': forms.Textarea(attrs={
                'rows': 10,
                'class': 'w-full bg-stone-900 text-stone-100 border border-stone-700 rounded-xl p-4 font-mono text-xs placeholder-stone-500 focus:outline-none focus:ring-2 focus:ring-blue-500 leading-relaxed transition',
                'placeholder': "Capo: 2nd Fret | Strumming: D-D-D-D-DU\n\n[Verse 1]\nEm7          G\nToday is gonna be the day...\n\n[Chorus]\nCadd9        Em7\nBecause maybe...",
                'required': True,
                'id': 'songContentInput'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['associated_chords'].queryset = Chord.objects.all().order_by('name')
        self.fields['associated_chords'].required = False
        self.fields['key'].required = False
