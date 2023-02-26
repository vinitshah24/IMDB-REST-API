from django.contrib import admin
from django.urls import path, include

from movies.views import movie_list, movie_details

urlpatterns = [
    path('', movie_list, name='movie-list'),
    path('<int:pk>', movie_details, name='movie-detail'),
]
