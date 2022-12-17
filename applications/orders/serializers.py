from rest_framework import serializers

from applications.orders.models import Order
from applications.product.models import Product
from applications.orders.tasks import send_confirm_link


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = Order
        exclude = ['confirm_code', 'order_confirm']

    def create(self, validated_data):
        order = Order.objects.create(**validated_data)
        order.create_confirm_code()
        order.save()
        send_confirm_link.delay(order.user.email, order.confirm_code)
        return order

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        product = Product.objects.get(id=rep['product']).title
        rep['product'] = product
        return rep

    def validate(self, attrs):
        product = attrs['product']
        count = attrs['count']
        if product.count < count:
            raise serializers.ValidationError(f'вы не можете заказать такое количество, осталось {product.count}')
        return attrs
