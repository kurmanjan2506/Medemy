from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rating import serializers
from rating.models import Like, Review
from rating.permissions import IsAuthor


class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = serializers.ReviewSerializer

    def get_permissions(self):
        if self.action in ('create', 'add_to_liked', 'remove_from_liked', 'favorite_action'):
            return [permissions.IsAuthenticated()]
        elif self.action in ('update', 'partial_update', 'destroy'):
            return [permissions.IsAuthenticated(), IsAuthor()]
        else:
            return [permissions.IsAuthenticatedOrReadOnly()]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


    # /reviews/<id>?add_to_liked/
    @action(['POST'], detail=True)
    def add_to_liked(self, request, pk):
        review = self.get_object()
        user = request.user
        if user.liked.filter(review=review).exists():
            return Response('This review is Already Liked!', status=400)
        Like.objects.create(owner=user, review=review)
        return Response('You Liked The Review', status=201)


    # /reviews/<id>?remove_from_liked/
    @action(['DELETE'], detail=True)
    def remove_from_liked(self, request, pk):
        review = self.get_object()
        user = request.user
        if not user.liked.filter(review=review).exists():
            return Response('You Didn\'t Like This review!', status=400)
        user.liked.filter(review=review).delete()
        return Response('Your Like is Deleted!', status=204)


    @action(['GET'], detail=True)
    def get_likes(self, request, pk):
        review = self.get_object()
        likes = review.likes.all()
        serializer = serializers.LikeSerializer(likes, many=True)
        return Response(serializer.data)
