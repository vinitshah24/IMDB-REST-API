from django.contrib import admin
from movies.models import VideoContent, StreamPlatform, Review

admin.site.register(VideoContent)
admin.site.register(StreamPlatform)
admin.site.register(Review)
