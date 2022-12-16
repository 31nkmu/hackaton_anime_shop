from rest_framework import serializers

from applications.likes.models import Like


class FanSerializer(serializers.Serializer):
    user = serializers.CharField(required=True)
