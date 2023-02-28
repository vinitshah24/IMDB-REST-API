from rest_framework import serializers

from movies.models import VideoContent, StreamPlatform, Review, Genre


class ReviewSerializer(serializers.ModelSerializer):
    review_user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        exclude = ('video_content',)


class VideoContentSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    # genre = serializers.StringRelatedField()
    # platform = serializers.StringRelatedField()

    class Meta:
        model = VideoContent
        fields = "__all__"


class StreamPlatformSerializer(serializers.ModelSerializer):
    # user related_name set in models
    # By default nested serializers are read-only
    video_content = VideoContentSerializer(many=True, read_only=True)
    # returns __str__ method value in nested object
    # video_content = serializers.StringRelatedField(many=True,read_only=True)
    # PK of the objects
    # video_content = serializers.PrimaryKeyRelatedField(many=True,read_only=True)
    # use the name set in url patterns for that view. Shows the url link to access the individual object
    # video_content = serializers.HyperlinkedIdentityField(many=True,read_only=True, view_name='video-content-detail')

    class Meta:
        model = StreamPlatform
        fields = "__all__"


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = "__all__"
