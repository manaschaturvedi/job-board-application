from datetime import datetime

from django.db import models


class UpdateInfo(models.Model):
    """ abstract model """
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(blank=True, auto_now_add=True)
    modified_at = models.DateTimeField(blank=True, auto_now=True)
    def to_dict(self):
        return self.__dict__

    def __unicode__(self):
        s = ''
        for k, v in self.__dict__.items():
            s += ('%s: %s\n' % (k, v))
        return s
    class Meta:
        abstract = True


class JobListings(UpdateInfo):
    job_id = models.CharField(max_length=100, default='')
    company_name = models.CharField(max_length=100)
    headline = models.TextField()
    description = models.TextField()
    job_role = models.CharField(max_length=100)
    link = models.TextField()
    location = models.CharField(max_length=200, blank=True)
    source = models.CharField(max_length=100, blank=True)
    salary = models.CharField(max_length=100, blank=True)
    job_type = models.CharField(max_length=100, blank=True)
    job_category = models.CharField(max_length=100, blank=True)
    skills = models.TextField()
    job_posted_on = models.DateTimeField(default=datetime.now)

    class Meta:
        db_table = "job_listings"


class EmailLeads(UpdateInfo):
    email = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = "email_leads"