from rest_framework import serializers

from applications.likes.models import Like
from applications.likes.services import is_fan
from applications.product.models import Product, Image


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, required=False)

    class Meta:
        model = Product
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        product = Product.objects.create(**validated_data)
        files = request.FILES
        for image in files.getlist('images'):
            Image.objects.create(product=product, image=image)
        return product

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        user = self.context.get('request').user
        images = []
        for i in rep['images']:
            images.append(i['image'])
        rep['images'] = images
        rep['likes'] = Like.objects.filter(product=instance, like=True).count()
        rep['is_fan'] = is_fan(user=user, obj=instance)
        return rep