from rest_framework import serializers

from main.models import UserMapping


class UserMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserMapping
        fields = "__all__"
