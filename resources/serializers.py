from rest_framework import serializers

from core.models import Resource

class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = ['id', 'name', 'quantity', 'survivor']
        read_only_fields = ['id']
        