from django.db import models

# Create your models here.

ROLES = (
    ('Android Engineer', 'Android Engineer'),
    ('Backend Engineer', 'Backend Engineer'),
    ('Data Engineer', 'Data Engineer'),
    ('DevOps', 'DevOps'),
    ('Engineering Manager', 'Engineering Manager'),
    ('Frontend Engineer', 'Frontend Engineer'),
    ('Full Stack Engineer', 'Full Stack Engineer'),
    ('iOS Engineer', 'iOS Engineer'),
    ('Machine Learning Engineer', 'Machine Learning Engineer'),
    ('Product Manager', 'Product Manager'),
    ('QA Engineer', 'QA Engineer'),
    ('Other', 'Other'),
)

class CandidateProfile(models.Model):
    candidate_id = models.CharField(max_length=255, blank=False)
    name = models.CharField(max_length=255)
    resume = models.FileField(upload_to='resumes/')
    location = models.CharField(max_length=255)
    preferred_role = models.CharField(max_length=255, choices=ROLES)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

