from django import forms
from .models import StudentProgress

class StudentProgressForm(forms.ModelForm):
    class Meta:
        model = StudentProgress
        fields = ['task', 'proof_of_submission', 'reason_for_late_submission']
        widgets = {
            'reason_for_late_submission': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Explain if delayed'}),
        }
