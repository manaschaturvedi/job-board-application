import pandas as pd
import json
from datetime import datetime
import pickle

from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.core.validators import URLValidator
from django.db.models import Q

from zeroxpapp.models import JobListings, EmailLeads
from zeroxpapp.utils import *
from zeroxpapp.ml_utilities import jd_keywords


@method_decorator(csrf_exempt, name='dispatch')
class LandingPage(View):

	def featured_skills(self):
		jobs = JobListings.objects.filter(active=True).values('skills')
		skills = {}
		for item in jobs:
			for key in item['skills'].split(','):
				if key in skills:
					skills[key] += 1
				else:
					skills[key] = 1
		ordered_skills = sorted(skills, key=skills.get)[::-1]
		final_skills = []
		for item in ordered_skills[:5]:
			final_skills.append({'skill': item, 'count': skills[item]})
		return final_skills

	def get(self, request):
		print('get params: {}'.format(request.GET))
		feat_skills = self.featured_skills()
		print('featured skills: {}'.format(feat_skills))
		caption = "We'll never share your email with anyone else"
		if 'q' in request.GET:
			keyword = request.GET['q']
			jobs = JobListings.objects.filter(
						Q(company_name__icontains=keyword) | Q(headline__icontains=keyword) |
						Q(description__icontains=keyword) | Q(job_role__icontains=keyword) |
						Q(location__icontains=keyword) | Q(skills__icontains=keyword)
					).order_by('-created_at')
		else:
			jobs = JobListings.objects.order_by('-created_at')

		job_listings = []
		for job in jobs:
			data = job.__dict__
			if not is_valid_url(data['link']):
				data['description'] += '\n' + data['link']
				data['link'] = ''
			data['location'] = data['location'][:20]
			data['job_posted_on'] = data['job_posted_on'].strftime("%B %d, %Y")
			job_listings.append(data)

		no_results_copy = 'No results found' if len(job_listings) == 0 else ''

		return render(
			request, 
			'index.html', 
			{
				'job_listings': job_listings, 
				'caption': caption, 
				'no_results_copy': no_results_copy,
				'feat_skills': feat_skills
			}
		)
	
	def post(self, request):
		feat_skills = self.featured_skills()
		job_listings = []
		search_input_value = ''
		if 'search_keyword' in request.POST:
			keyword = request.POST['search_keyword']
			search_input_value = keyword
			jobs = JobListings.objects.filter(
						Q(company_name__icontains=keyword) | Q(headline__icontains=keyword) |
						Q(description__icontains=keyword) | Q(job_role__icontains=keyword) |
						Q(location__icontains=keyword) | Q(skills__icontains=keyword)
					).order_by('-created_at')
		else:
			jobs = JobListings.objects.order_by('-created_at')
		for job in jobs:
			data = job.__dict__
			if not is_valid_url(data['link']):
				data['description'] += '\n' + data['link']
				data['link'] = ''
			# data['description'] = data['description'][:200] + '...'
			data['job_posted_on'] = data['job_posted_on'].strftime("%B %d, %Y")
			job_listings.append(data)
		print('form data:: {}'.format(request.POST))
		if 'email' in request.POST:
			user_email = request.POST['email']
			lead = EmailLeads(email=user_email)
			lead.save()
			caption = 'You are now successfully subscribed to our latest updates'
			return render(request, 'index.html', {'job_listings': job_listings, 'caption': caption})
		else:
			caption = "We'll never share your email with anyone else"
			print('search keyword: {}'.format(request.POST['search_keyword']))

		no_results_copy = 'No results found' if len(job_listings) == 0 else ''

		return render(
			request, 
			'index.html', 
			{
				'job_listings': job_listings, 
				'caption': caption,
				'search_input_value': search_input_value,
				'no_results_copy': no_results_copy,
				'feat_skills': feat_skills
			}
		)


@method_decorator(csrf_exempt, name='dispatch')
class PostNewJob(View):

	def derive_job_skills(self, description):
		obj = jd_keywords.JDTopKeywords(description)
		return obj.fetch_top_keywords()

	def get(self, request):
		return render(request, 'post_job.html')

	def post(self, request):
		print('form data:: {}'.format(request.POST))
		form_data = request.POST
		company_name = form_data['company_name']
		description = form_data['description']
		job_role = form_data['job_role']
		link = form_data['link']
		location = form_data['location']
		source = 'form_submit'
		salary = form_data['salary']
		job_type = form_data['job_type']
		job_category = form_data['job_category']
		skills = form_data['skills']
		if not skills:
			skills = self.derive_job_skills(description)
		skills = skills.lower().replace(', ', ',')
		print(skills)
		# skills = self.derive_job_skills(description)
		new_job_post = JobListings(
			company_name = company_name,
			description = description,
			job_role = job_role,
			link = link,
			location = location,
			source = source,
			salary = salary,
			job_type = job_type,
			job_category = job_category,
			skills = skills
		)
		new_job_post.save()
		return redirect('post_new_job')


@method_decorator(csrf_exempt, name='dispatch')
class DataSeeding(View):

	def derive_job_skills(self, description):
		obj = jd_keywords.JDTopKeywords(description)
		return obj.fetch_top_keywords()

	def get(self, request):
		github_jobs = pd.read_csv('zeroxpapp/csv_files/github_jobs.csv')
		for job in github_jobs.iterrows():
			try:
				item = job[1]
				skills = self.derive_job_skills(item.description)
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
					'skills': skills,
					# 'job_posted_on': ''
				}
				obj = JobListings(**data)
				obj.save()
			except Exception as e:
				print('error: {}'.format(e))
		return HttpResponse(json.dumps({'success':True}))
