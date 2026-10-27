from django import forms
from .models import PracticeSession

class PracticeSessionForm(forms.ModelForm):
    class Meta:
        model = PracticeSession
        fields = ['duration_minutes', 'focus_area', 'notes']
        widgets = {
            'duration_minutes': forms.NumberInput(attrs={
                'class': 'w-full bg-white dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-lg px-3.5 py-2.5 text-gray-900 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition text-base',
                'placeholder': 'e.g. 30',
                'min': '1',
                'max': '600',
                'id': 'id_duration_minutes',
            }),
            'focus_area': forms.Select(attrs={
                'class': 'w-full bg-white dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-lg px-3.5 py-2.5 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition text-base cursor-pointer',
                'id': 'id_focus_area',
            }),
            'notes': forms.Textarea(attrs={
                'rows': 3,
                'class': 'w-full bg-white dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-lg px-3.5 py-2.5 text-gray-900 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition text-base',
                'placeholder': 'Optional: What did you practice? (e.g., F chord barre transition, pentatonic scale, fingerpicking)',
                'id': 'id_notes',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ensure all fields have the dark mode text and background styles
        for name, field in self.fields.items():
            if 'class' in field.widget.attrs:
                continue
            field.widget.attrs['class'] = 'w-full bg-white dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-lg px-3.5 py-2.5 text-gray-900 dark:text-gray-100 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500'
