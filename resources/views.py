from rest_framework.generics import RetrieveAPIView, ListAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from helpers.verify_survivor_exist import survivor_exists
from helpers.verify_survivor_infected import survivor_infected

from resources.helpers.get_count_survirvos import get_survivor_amount

from .serializers import ResourceSerializer, NegotiateSerializer
from core.models import Survivor, Resource
from .helpers.get_resources_average import resource_average

class ListSurvivorResources(RetrieveAPIView):
    """ list resources of an survivor """
    serializer_class = ResourceSerializer
    queryset = Resource.objects.all()

    def get(self, request, *args, **kwargs):
        if survivor_exists(survivor_id=kwargs['pk']):
            if survivor_infected(survivor_id=kwargs['pk']):
                return Response(data={'detail': 'Sobrevivente infectado, recursos indisponíveis.'}, status=status.HTTP_400_BAD_REQUEST)
            resources = self.queryset.filter(survivor=kwargs['pk'])
            serializer = self.serializer_class(instance=resources, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(data={'detail': 'Sobrevivente não encontrado.'}, status=status.HTTP_404_NOT_FOUND)


class MeanAmountResources(ListAPIView):
    """ list average of all resources """
    queryset = Resource.objects.all()
    serializer_class = None

    def get(self, request, *args, **kwargs):
        survivor_amount = get_survivor_amount()
        if survivor_amount == 0:
            return Response(data={'Água': 0, 'Medicação': 0, 'Alimentação': 0, 'Munição': 0}, status=status.HTTP_200_OK)
        else:
            water = resource_average(resource_name='Água', survivor_amount=survivor_amount)
            medication = resource_average(resource_name='Medicação', survivor_amount=survivor_amount)
            food = resource_average(resource_name='Alimentação', survivor_amount=survivor_amount)
            ammunition = resource_average(resource_name='Munição', survivor_amount=survivor_amount)
            return Response(data={'Água': water, 'Medicação': medication, 'Alimentação': food, 'Munição': ammunition}, status=status.HTTP_200_OK)


class NegotiateResources(CreateAPIView):
    """ make an resource negotiation """
    queryset = None
    serializer_class = NegotiateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            return Response(data={'detail': 'Negociação realizada com sucesso.'}, status=status.HTTP_201_CREATED)
        return Response(data={'detail': serializer.errors['detail'][0]}, status=status.HTTP_400_BAD_REQUEST)
