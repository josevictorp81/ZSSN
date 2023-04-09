from rest_framework import serializers

from core.models import Infected, Resource, Survivor
from .helpers.search_survivor import survivor_exists
from .helpers.save_survivor_infected import save_survivor_infected
from .helpers.survivor_infected_verify import survivor_infected_verify

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
        reporter = attrs['reporter']
        infected = attrs['infected']
        if reporter == infected:
            raise serializers.ValidationError(detail={'detail': 'Sobrevivente não pode reportar a si mesmo como infectado.'})
        if survivor_infected_verify(id=reporter):
            raise serializers.ValidationError(detail={'detail': 'Sobrevivente infectado não pode reportar outro sobrevivente como infectado.'})
        if not survivor_exists(survivor=reporter):
            raise serializers.ValidationError(detail={'detail': 'Sobrevivente que reportou a infecção não existe.'})
        if not survivor_exists(survivor=infected):
            raise serializers.ValidationError(detail={'detail': 'Sobrevivente reportado como infectado não existe.'})
        reported = self.Meta.model.objects.filter(reporter=reporter,  infected=infected)
        if reported.exists():
            raise serializers.ValidationError(detail={'detail': f'Sobrevivente {reporter} ja reportou o sobrevivente {infected} como infectado.'})
        return super().validate(attrs)

    def create(self, validated_data):
        infected = Infected.objects.create(**validated_data)
        infected_count = Infected.objects.filter(infected=validated_data['infected'])
        if infected_count.count() < 3:
            return infected
        else:
            save_survivor_infected(validated_data['infected'])
            return infected
        