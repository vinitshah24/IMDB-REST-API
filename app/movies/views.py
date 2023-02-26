from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics, mixins, viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle, ScopedRateThrottle
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import ValidationError
from drf_spectacular.utils import extend_schema, extend_schema_view

from movies.serializers import VideoContentSerializer, StreamPlatformSerializer, ReviewSerializer, GenreSerializer
from movies.models import StreamPlatform, VideoContent, Review, Genre
from movies.permissions import IsAdminOrReadOnly, IsReviewUserOrReadOnly
from movies.throttling import ReviewCreateThrottle, ReviewListThrottle
from movies.pagination import WatchListPagination, WatchListLOPagination, WatchListCPagination

# class StreamPlatformAPIView(APIView):

#     def get(self, request):
#         platform = StreamPlatform.objects.all()
#         # serializers.HyperlinkedIdentityField requires context={'request': request}
#         serializer = StreamPlatformSerializer(platform, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = StreamPlatformSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)


# class StreamPlatformDetailAPIView(APIView):

#     def get(self, request, pk):
#         try:
#             platform = StreamPlatform.objects.get(pk=pk)
#         except StreamPlatform.DoesNotExist:
#             return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
#         # serializers.HyperlinkedIdentityField requires context={'request': request}
#         serializer = StreamPlatformSerializer(platform)
#         return Response(serializer.data)

#     def put(self, request, pk):
#         platform = StreamPlatform.objects.get(pk=pk)
#         serializer = StreamPlatformSerializer(platform, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk):
#         platform = StreamPlatform.objects.get(pk=pk)
#         platform.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# class StreamPlatformViewSet(viewsets.ViewSet):
#     # we woulds have to manually implement all methods we want

#     def list(self, request):
#         queryset = StreamPlatform.objects.all()
#         serializer = StreamPlatformSerializer(queryset, many=True)
#         return Response(serializer.data)

#     def retrieve(self, request, pk=None):
#         queryset = StreamPlatform.objects.all()
#         video_content = get_object_or_404(queryset, pk=pk)
#         serializer = StreamPlatformSerializer(video_content)
#         return Response(serializer.data)

#     def create(self, request):
#         serializer = StreamPlatformSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)

@extend_schema(tags=['Genre'])
@extend_schema_view(
    list=extend_schema(description='view list description'),
    retrieve=extend_schema(description='view retrieve description'),
    extended_action=extend_schema(description='view extended action description'),
    raw_action=extend_schema(description='view raw action description'),
)
class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

    # def get_queryset(self):
    #     Genre.refresh_from_db()
    #     return Genre.objects.all()

    # permission_classes = [IsAdminOrReadOnly]
    # throttle_classes = [AnonRateThrottle]


@extend_schema(tags=['Stream Platform'])
@extend_schema_view(
    list=extend_schema(description='view list description'),
    retrieve=extend_schema(description='view retrieve description'),
    extended_action=extend_schema(description='view extended action description'),
    raw_action=extend_schema(description='view raw action description'),
)
class StreamPlatformViewSet(viewsets.ModelViewSet):
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer
    permission_classes = [IsAdminOrReadOnly]
    throttle_classes = [AnonRateThrottle]


@extend_schema(tags=['Video Content'])
class VideoContentListAPIView(APIView):

    permission_classes = [IsAdminOrReadOnly]
    throttle_classes = [AnonRateThrottle]

    def get(self, request):
        movies = VideoContent.objects.all()
        serializer = VideoContentSerializer(movies, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = VideoContentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


@extend_schema(tags=['Video Content'])
class VideoContentDetailAPIView(APIView):

    permission_classes = [IsAdminOrReadOnly]
    throttle_classes = [AnonRateThrottle]

    def get(self, request, pk):
        try:
            movie = VideoContent.objects.get(pk=pk)
        except VideoContent.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = VideoContentSerializer(movie)
        return Response(serializer.data)

    def put(self, request, pk):
        movie = VideoContent.objects.get(pk=pk)
        serializer = VideoContentSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        movie = VideoContent.objects.get(pk=pk)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, pk):
        movie = VideoContent.objects.get(pk=pk)
        serializer = VideoContentSerializer(movie, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)

# class ReviewDetail(mixins.RetrieveModelMixin, generics.GenericAPIView):
#     """Basically we are using the GenericAPIView and overriding the get method"""
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         # You have to override the get method using the RetrieveModelMixin
#         return self.retrieve(request, *args, **kwargs)


# class ReviewList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
#     """Basically we are using the GenericAPIView and overriding the get and post method"""
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)


@extend_schema(tags=['Review'])
class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [ReviewCreateThrottle]

    def get_queryset(self):
        return Review.objects.all()

    def perform_create(self, serializer):
        """ Overrriden - called by CreateModelMixin when saving a new object instance """
        pk = self.kwargs.get('pk')
        movie = VideoContent.objects.get(pk=pk)
        # checks whether the user has already reviewed the movie ands raises an error if so
        review_user = self.request.user
        review_queryset = Review.objects.filter(video_content=movie, review_user=review_user)
        if review_queryset.exists():
            raise ValidationError("You have already reviewed this movie!")
        # Default value for rating is 0 so check if user has rated something else and update
        if movie.ratings_count == 0:
            movie.avg_ratings = serializer.validated_data['rating']
        else:
            movie.avg_ratings = (movie.avg_ratings + serializer.validated_data['rating'])/2
        movie.ratings_count += 1
        # serializer will validate the data and call create or update method accordingly
        movie.save()
        serializer.save(video_content=movie, review_user=review_user)


@extend_schema(tags=['Review'])
class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsReviewUserOrReadOnly]
    throttle_classes = [ScopedRateThrottle, AnonRateThrottle]
    throttle_scope = 'review-detail-throttle'


@extend_schema(tags=['Review'])
class ReviewList(generics.ListAPIView):

    serializer_class = ReviewSerializer
    throttle_classes = [ReviewListThrottle, AnonRateThrottle]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['review_user__username', 'active']

    def get_queryset(self):
        """ Overriding the queryset """
        pk = self.__getattribute__('kwargs').get('pk')
        return Review.objects.filter(video_content=pk)
