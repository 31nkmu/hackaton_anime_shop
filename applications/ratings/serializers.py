from rest_framework import serializers


class ReviewerSerializer(serializers.Serializer):
    user = serializers.CharField()
