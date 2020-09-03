from django import forms
from .models import JobListings


class JobListingsForm(forms.ModelForm):

    class Meta:
        model = JobListings
        fields = (
            'company_name', 'headline', 'description', 'job_role', 'link', 'location', 'salary',
            'job_type', 'job_category', 'skills'
        )
