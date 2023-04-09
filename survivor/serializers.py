from rest_framework import serializers

from core.models import Infected, Resource, Survivor
from .helpers.search_survivor import survivor_exists
from .helpers.save_survivor_infected import save_survivor_infected

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


class InfectedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Infected
        fields = "__all__"
        read_only = ['id']

    def validate(self, attrs):
        if not survivor_exists(survivor=attrs['reporter']):
            raise serializers.ValidationError(detail={'detail': 'Sobrevivente que reportou a infecção não existe.'})
        if not survivor_exists(survivor=attrs['infected']):
            raise serializers.ValidationError(detail={'detail': 'Sobrevivente reportado como infectado não existe.'})
        return super().validate(attrs)

    def create(self, validated_data):
        infected = Infected.objects.create(**validated_data)
        infected_count = Infected.objects.filter(infected=validated_data['infected'])
        if infected_count.count() < 3:
            return infected
        else:
            save_survivor_infected(validated_data['infected'])
            return infected
        