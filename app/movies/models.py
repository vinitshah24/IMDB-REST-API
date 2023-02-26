from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User


class StreamPlatform(models.Model):
    name = models.CharField(max_length=30)
    about = models.CharField(max_length=150)
    website = models.URLField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "STREAM_PLATFORM"


class VideoContent(models.Model):
    title = models.CharField(max_length=50)
    storyline = models.CharField(max_length=200)
    platform = models.ForeignKey(StreamPlatform,
                                 on_delete=models.CASCADE,
                                 related_name="video_content")
    active = models.BooleanField(default=True)
    avg_ratings = models.FloatField(default=0)
    ratings_count = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "VIDEO_CONTENT"


class Review(models.Model):
    review_user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    description = models.CharField(max_length=200, null=True)
    video_content = models.ForeignKey(
        VideoContent, on_delete=models.CASCADE, related_name="reviews")
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.rating}  | {self.video_content.title} | {self.review_user}"

    class Meta:
        db_table = "REVIEW"


class Genre(models.Model):
    genre_id = models.AutoField(primary_key=True)
    genre_name = models.CharField(max_length=60)

    def __str__(self):
        return self.genre_name

    class Meta:
        db_table = "GENRE"
        # If False, no database table creation or deletion operations will be performed for this model.
        # This is useful if the model represents an existing table or a database view that has been created by
        # some other means.
        managed = True
