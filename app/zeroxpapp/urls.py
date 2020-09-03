from django.urls import include, path
from zeroxpapp.views import *

urlpatterns = [
    path('data_seeding/', DataSeeding.as_view()),
    path('post_new_job/', PostNewJob.as_view(), name='post_new_job'),
]
