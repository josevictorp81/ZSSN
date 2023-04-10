from rest_framework import serializers

from core.models import Infected, Survivor
from helpers.verify_survivor_exist import survivor_exists
from survivors.helpers.save_resources import save_resources
from .helpers.save_survivor_infected import save_survivor_infected
from helpers.verify_survivor_infected import survivor_infected
from resources.serializers import ResourceNegotiateSerializer

class SurvivorSerializer(serializers.ModelSerializer):
    resources = ResourceNegotiateSerializer(many=True, required=False)
    class Meta:
        model = Survivor
        fields = ['id', 'name', 'age', 'sex', 'local', 'resources']
        read_only_fields = ['id']
    
    def validate(self, attrs):
        if not attrs['resources'] or len(attrs['resources']) == 0:
            raise serializers.ValidationError(detail={'detail': 'Informe os recursos do sobrevivente.'})
        return super().validate(attrs)
    
    def create(self, validated_data):
        survivor = Survivor.objects.create(name=validated_data['name'], age=validated_data['age'], sex=validated_data['sex'], local=validated_data['local'])
        save_resources(resources=validated_data['resources'], survivor_id=survivor.id)
        return survivor


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
        if  survivor_infected(survivor_id=reporter):
            raise serializers.ValidationError(detail={'detail': 'Sobrevivente infectado não pode reportar outro sobrevivente como infectado.'})
        if not survivor_exists(survivor_id=reporter):
            raise serializers.ValidationError(detail={'detail': 'Sobrevivente que reportou a infecção não existe.'})
        if not survivor_exists(survivor_id=infected):
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
        