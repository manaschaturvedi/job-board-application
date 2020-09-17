from django.urls import include, path
from candidates.views import *

urlpatterns = [
    path('login/', CandidateLogin.as_view()),
    path('dashboard/', Dashboard.as_view(), name='candidate_dashboard'),
]
