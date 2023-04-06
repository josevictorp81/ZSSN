from rest_framework import serializers

from core.models import Resource, Survivor

class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = ['id', 'name', 'quantity', 'survivor']
        read_only_fields = ['id']


class SurvivorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Survivor
        fields = ['id', 'name', 'age', 'sex', 'local']
        read_only_fields = ['id']


class UpdateLocalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Survivor
        fields = ['id', 'name', 'age', 'sex', 'local']
        read_only_fields = ['id', 'name', 'age', 'sex']
