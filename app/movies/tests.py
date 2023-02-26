from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User

from movies import models
from movies import serializers


class StreamPlatformTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="example", password="Password@123")
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.stream = models.StreamPlatform.objects.create(name="Netflix",
                                                           about="#1 Platform",
                                                           website="https://www.netflix.com")

    def test_stream_create(self):
        data = {
            "name": "Netflix",
            "about": "#1 Streaming Platform",
            "website": "https://netflix.com"
        }
        response = self.client.post(reverse('stream-list'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_stream_list(self):
        response = self.client.get(reverse('stream-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_stream_ind(self):
        response = self.client.get(reverse('stream-detail', args=(self.stream.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class MovieListTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="example", password="Password@123")
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.stream = models.StreamPlatform.objects.create(name="Netflix",
                                                           about="#1 Platform",
                                                           website="https://www.netflix.com")
        self.movie = models.VideoContent.objects.create(platform=self.stream,
                                                        title="Example Movie",
                                                        storyline="Example Movie",
                                                        active=True)

    def test_movie_create(self):
        data = {
            "platform": self.stream,
            "title": "Example Movie",
            "storyline": "Example Story",
            "active": True
        }
        response = self.client.post(reverse('video-content-list'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_movie_list(self):
        response = self.client.get(reverse('video-content-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_movie_detail(self):
        response = self.client.get(reverse('video-content-detail', args=(self.movie.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(models.VideoContent.objects.count(), 1)
        self.assertEqual(models.VideoContent.objects.get().title, 'Example Movie')


class ReviewTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="example", password="Password@123")
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.stream = models.StreamPlatform.objects.create(name="Netflix",
                                                           about="#1 Platform",
                                                           website="https://www.netflix.com")
        self.video_content = models.VideoContent.objects.create(platform=self.stream,
                                                        title="Example Movie",
                                                        storyline="Example Movie",
                                                        active=True)
        self.video_content2 = models.VideoContent.objects.create(platform=self.stream,
                                                         title="Example Movie",
                                                         storyline="Example Movie",
                                                         active=True)
        self.review = models.Review.objects.create(review_user=self.user,
                                                   rating=5,
                                                   description="Great Movie",
                                                   video_content=self.video_content2,
                                                   active=True)

    def test_review_create(self):
        data = {
            "review_user": self.user,
            "rating": 5,
            "description": "Great Movie!",
            "video_content": self.video_content,
            "active": True
        }
        response = self.client.post(reverse('review-create', args=(self.video_content.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.Review.objects.count(), 2)
        response = self.client.post(reverse('review-create', args=(self.video_content.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_review_create_unauth(self):
        data = {
            "review_user": self.user,
            "rating": 5,
            "description": "Great Movie!",
            "video_content": self.video_content,
            "active": True
        }
        self.client.force_authenticate(user=None)
        response = self.client.post(reverse('review-create', args=(self.video_content.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_review_update(self):
        data = {
            "review_user": self.user,
            "rating": 4,
            "description": "Great Movie! - Updated",
            "video_content": self.video_content,
            "active": False
        }
        response = self.client.put(reverse('review-detail', args=(self.review.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_review_list(self):
        response = self.client.get(reverse('review-list', args=(self.video_content.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_review_detail(self):
        response = self.client.get(reverse('review-detail', args=(self.review.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_review_delete(self):
        response = self.client.delete(reverse('review-detail', args=(self.review.id,)))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    # def test_review_user(self):
    #     response = self.client.get('/watch/reviews/?username' + self.user.username)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
