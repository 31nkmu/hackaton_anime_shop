from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from applications.favorites import services


class FavoriteMixin:
    @action(detail=True, methods=['POST'])
    def favorite(self, request, pk=None):
        obj = self.get_object()
        user = request.user
        status_ = services.add_del_favorite(user=user, obj=obj)
        return Response(
            {
                'status': status_,
                'user': user.email,
                'product': obj.title
            },
            status=status.HTTP_200_OK
        )

    @action(detail=False, methods=['GET'])
    def get_favorites(self, request):
        product_data = services.get_favorites(user=request.user)
        return Response(product_data, status=status.HTTP_200_OK)
