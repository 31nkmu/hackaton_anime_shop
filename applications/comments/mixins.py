from django.utils.datastructures import MultiValueDictKeyError
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from applications.comments import services


class CommentMixin:
    @action(detail=True, methods=['POST'])
    def give_comment(self, request, pk=None):
        try:
            comment = request.data['comment']
            user = request.user
            obj = self.get_object()
            status_ = services.give_comment(user=user, obj=obj, comment=comment)
            return Response({
                'status': status_,
                'user': user.email,
                'comment': comment
            }, status=status.HTTP_200_OK)
        except MultiValueDictKeyError:
            return Response('поле comment обязательно')

    @action(detail=True, methods=['POST'])
    def del_comment(self, request, pk=None):
        user = request.user
        obj = self.get_object()
        services.del_comment(obj=obj, user=user)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['GET'])
    def commentators(self, request, pk=None):
        return Response(services.get_commentators(obj=self.get_object()), status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'])
    def comments(self, request):
        return Response(services.get_comments(user=request.user), status=status.HTTP_200_OK)
