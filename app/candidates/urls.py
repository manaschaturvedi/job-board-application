from django.urls import include, path
from candidates.views import *

urlpatterns = [
    path('login/', CandidateLogin.as_view()),
]
