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
from django.core.files.storage import FileSystemStorage
from candidates.forms import CandidateProfileForm
from candidates.models import CandidateProfile


@method_decorator(csrf_exempt, name='dispatch')
class CandidateLogin(View):
	def get(self, request):
		return render(request, 'candidate_login.html')

	def post(self, request):
		pass


@method_decorator(csrf_exempt, name='dispatch')
class Dashboard(View):
	def get(self, request):
		if request.user.is_authenticated:
			candidate_id = request.user.id
			candidate_data = CandidateProfile.objects.filter(candidate_id=candidate_id).last()
			if candidate_data:
				candidate_data = candidate_data.__dict__
				data = {
					'name': candidate_data['name'],
					'location': candidate_data['location'],
					'preferred_role': candidate_data['preferred_role'],
					'resume': candidate_data['resume'],
				}
				form = CandidateProfileForm(initial=data)
			else:
				form = CandidateProfileForm()
			return render(request, 'candidate_dashboard.html', {'form': form})
		else:
			return render(request, 'candidate_login.html')

	def post(self, request):
		form = CandidateProfileForm(request.POST, request.FILES)
		# print(form.__dict__)
		if form.is_valid():
			obj = form.save(commit=False)
			obj.candidate_id = request.user.id
			obj.save()

		return render(request, 'candidate_dashboard.html', {'form': form})
