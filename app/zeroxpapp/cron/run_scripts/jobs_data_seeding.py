import pandas as pd

# from zeroxpapp.models import JobListings
'''
job_id = models.CharField(max_length=100)
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
    job_posted_on = models.DateTimeField(blank=True)
'''

github_jobs = pd.read_csv('github_jobs.csv')
for job in github_jobs.iterrows():
    item = job[1]
    data = {
        'job_id': item.job_id,
        'company_name': item.company,
        'headline': '',
        'description': item.description,
        'job_role': item.job_role,
        'link': item.link,
        'location': item.location,
        'source': item.source,
        'salary': '',
        'job_type': item.job_type,
        'job_category': '',
        'skills': '',
        'job_posted_on': item.date_posted
    }
    print(data)
    break

# print(github_jobs)
