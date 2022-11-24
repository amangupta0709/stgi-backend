from rest_framework import serializers

from main.models import UserMapping


class UserMappingSerializer(serializers.ModelSerializer):
    mapping_name = serializers.SerializerMethodField()

    class Meta:
        model = UserMapping
        fields = "__all__"

    def get_mapping_name(self, obj):
        return obj.file.name
