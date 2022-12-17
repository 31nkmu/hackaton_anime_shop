from rest_framework import serializers


class FavoriteSerializer(serializers.Serializer):
    product = serializers.CharField()
