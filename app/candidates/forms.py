from django import forms
from candidates.models import CandidateProfile


class CandidateProfileForm(forms.ModelForm):
    class Meta:
        model = CandidateProfile
        fields = ('name', 'location', 'preferred_role', 'resume',)
