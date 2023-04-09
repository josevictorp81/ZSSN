from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import ResourceSerializer
from core.models import Survivor, Resource
from .helpers.get_resources_average import mean_ammunition, mean_food, mean_medication, mean_water

class ListSurvivorResources(RetrieveAPIView):
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
    queryset = Resource.objects.all()
    serializer_class = None

    def get(self, request, *args, **kwargs):
        return Response(data={'água': mean_water(), 'medicação': mean_medication(), 'alimentação': mean_food(), 'munição': mean_ammunition()}, status=status.HTTP_200_OK)