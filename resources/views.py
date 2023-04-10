from rest_framework.generics import RetrieveAPIView, ListAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import ResourceSerializer, NegotiateSerializer
from core.models import Survivor, Resource
from .helpers.get_resources_average import resource_average

class ListSurvivorResources(RetrieveAPIView):
    """ list resources of an survivor """
    serializer_class = ResourceSerializer
    queryset = Resource.objects.all()

    def get(self, request, *args, **kwargs):
        if Survivor.objects.filter(id=kwargs['pk']).exists():
            if Survivor.objects.filter(id=kwargs['pk']).first().infected:
                return Response(data={'detail': 'Sobrevivente infectado, recursos indisponíveis.'}, status=status.HTTP_200_OK)
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
        water = resource_average(resource_name='Água')
        medication = resource_average(resource_name='Medicação')
        food = resource_average(resource_name='Alimentação')
        ammunition = resource_average(resource_name='Munição')
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
