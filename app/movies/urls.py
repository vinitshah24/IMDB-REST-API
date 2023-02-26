from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from movies.views import (VideoContentListAPIView,
                          VideoContentDetailAPIView,
                          #   StreamPlatformAPIView,
                          #   StreamPlatformDetailAPIView,
                          StreamPlatformViewSet,
                          GenreViewSet)
from movies.views import ReviewList, ReviewDetail, ReviewCreate


router = DefaultRouter()
# basename used in tests for reverse urls
router.register('streams', StreamPlatformViewSet, basename='stream')
router.register('genres', GenreViewSet, basename='genre')


urlpatterns = [

    path('', VideoContentListAPIView.as_view(), name='video-content-list'),
    path('<int:pk>/', VideoContentDetailAPIView.as_view(), name='video-content-detail'),

    # path('stream/', StreamPlatformAPIView.as_view(), name='stream-list'),
    # path('stream/<int:pk>', StreamPlatformDetailAPIView.as_view(), name='stream-detail'),
    path('', include(router.urls)),

    # path('reviews/', ReviewList.as_view(), name='review-list'),
    # path('reviews/<int:pk>', ReviewDetail.as_view(), name='review-detail'),
    path('<int:pk>/reviews-create/', ReviewCreate.as_view(), name='review-create'),
    path('<int:pk>/reviews/', ReviewList.as_view(), name='review-list'),
    path('reviews/<int:pk>/', ReviewDetail.as_view(), name='review-detail'),
]
