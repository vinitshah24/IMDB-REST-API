from django.contrib import admin
from django.urls import path, include

from movies.views import MovieListAPIView, MovieDetailAPIView

urlpatterns = [
    path('', MovieListAPIView.as_view(), name='movie-list'),
    path('<int:pk>/', MovieDetailAPIView.as_view(), name='movie-detail'),
]
