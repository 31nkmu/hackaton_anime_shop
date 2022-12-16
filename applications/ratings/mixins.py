from django.utils.datastructures import MultiValueDictKeyError
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from applications.ratings import services
from applications.ratings.services import get_reviewers


class RatingMixin:
    @action(detail=True, methods=['POST'])
    def give_rating(self, request, pk=None):
        try:
            obj = self.get_object()
            user = request.user
            rating = request.data['rating']
            status_ = services.give_rating(obj=obj, user=user, rating=rating)
            return Response({'status': status_, 'rating': rating, 'user': user.email}, status=status.HTTP_200_OK)
        except MultiValueDictKeyError:
            return Response('поле rating обязательно')

    @action(detail=True, methods=['POST'])
    def del_rating(self, request, pk=None):
        user = request.user
        obj = self.get_object()
        services.del_rating(user=user, obj=obj)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['GET'])
    def reviewers(self, request, pk=None):
        obj = self.get_object()
        users_data = get_reviewers(obj=obj)
        return Response(users_data, status=status.HTTP_200_OK)
