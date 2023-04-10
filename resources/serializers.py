from rest_framework import serializers

from core.models import Resource
from helpers.verify_survivor_exist import survivor_exists
from helpers.verify_survivor_infected import survivor_infected
from .helpers.count_points import count_resources_points
from .helpers.update_negotiantion import update_resources
from .helpers.get_resources import get_resources


class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = ['id', 'name', 'quantity', 'survivor']
        read_only_fields = ['id']


class ResourceNegotiateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = ['name', 'quantity']


class NegotiateSerializer(serializers.Serializer):
    negotiator = serializers.IntegerField()
    target = serializers.IntegerField()
    negotiator_resources = ResourceNegotiateSerializer(many=True, required=True)
    target_resources = ResourceNegotiateSerializer(many=True, required=True)

    def validate(self, attrs):
        """ validate serializer data """
        if not survivor_exists(survivor_id=attrs['negotiator']) or not survivor_exists(survivor_id=attrs['target']):
            raise serializers.ValidationError(detail={'detail': 'Sobrevivente não existe.'})
        if  survivor_infected(survivor_id=attrs['negotiator']) or  survivor_infected(survivor_id=attrs['target']):
            raise serializers.ValidationError(detail={'detail': 'Negociação inválida, um dos sobreviventes está infectado.'})
        if len(attrs['negotiator_resources']) == 0 or len(attrs['target_resources']) == 0:
            raise serializers.ValidationError(detail={'detail': 'Negociação inválida, nenhum recurso enviado para troca.'})
        negotiator_points = count_resources_points(attrs['negotiator_resources'])
        target_points = count_resources_points(attrs['target_resources'])
        if negotiator_points != target_points:
             raise serializers.ValidationError(detail={'detail': 'Negociação inválida, quantidade de pontos dos sobrevivente é diferente.'})
        return super().validate(attrs)
    
    def create(self, validated_data):
        """ make a negotiation update """
        update_resources(survivor=validated_data['negotiator'], resources=validated_data['negotiator_resources'])
        update_resources(survivor=validated_data['target'], resources=validated_data['target_resources'])
        update_resources(survivor=validated_data['negotiator'], resources=validated_data['target_resources'])
        update_resources(survivor=validated_data['target'], resources=validated_data['negotiator_resources'])
        negotiator_resources = get_resources(survivor_id=validated_data['negotiator'])
        target_resources = get_resources(survivor_id=validated_data['target'])
        return {'negotiator': validated_data['negotiator'], 'target': validated_data['target'], 'negotiator_resources': negotiator_resources, 'target_resources': target_resources}
    