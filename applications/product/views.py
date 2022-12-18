from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from applications.comments.mixins import CommentMixin
from applications.favorites.mixins import FavoriteMixin
from applications.likes.mixins import LikeMixin
from applications.product.models import Product
from applications.product.serializers import ProductSerializer
from applications.ratings.mixins import RatingMixin


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 10000


class ProductViewSet(LikeMixin, RatingMixin, CommentMixin, FavoriteMixin, ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = LargeResultsSetPagination
    filter_backends = (OrderingFilter, SearchFilter, DjangoFilterBackend)
    filterset_fields = ['category']
    search_fields = ['title']
    ordering_fields = ['id', 'price']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['DELETE'])
    def del_images(self, request, pk=None):
        user = request.user
        product = self.get_object()
        if product.user == user:
            images = product.images.all()
            images.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'status': 'только владелец может удалить картинку'}, status=status.HTTP_400_BAD_REQUEST)
