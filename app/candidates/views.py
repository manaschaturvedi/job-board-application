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


@method_decorator(csrf_exempt, name='dispatch')
class CandidateLogin(View):

	def get(self, request):
		return render(request, 'candidate_login.html')

	def post(self, request):
		pass
