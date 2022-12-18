from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from applications.orders.models import Order
from applications.orders.serializers import OrderSerializer


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        res = queryset.filter(user=user)
        return res


class OrderConfirm(APIView):
    @staticmethod
    def get(request, confirm_code):
        try:
            order = Order.objects.get(confirm_code=confirm_code)
            order.order_confirm = True
            order.confirm_code = ''
            ordered_count = order.count
            product = order.product
            count = product.count
            product.count = count - ordered_count
            if product.count == 0:
                product.status = 'out_of_stock'
            product.save()
            order.save()
            return Response({'msg': 'заказ подтвержден'}, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            return Response({'msg': 'неправильный код подтверждения заказа'}, status=status.HTTP_400_BAD_REQUEST)
