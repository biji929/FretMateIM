from django import forms
from .models import PracticeSession

class PracticeSessionForm(forms.ModelForm):
    class Meta:
        model = PracticeSession
        fields = ['duration_minutes', 'focus_area', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
