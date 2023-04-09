from rest_framework.generics import CreateAPIView, UpdateAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import SurvivorSerializer, UpdateLocalSerializer, ResourceSerializer, InfectedSerializer
from core.models import Survivor, Resource, Infected
from .helpers.save_resources import save_resources
from .helpers.survivor_object import create_survivor_object


class SurvivorCreate(CreateAPIView):
    serializer_class = SurvivorSerializer
    queryset = Survivor.objects.all()

    def create(self, request, *args, **kwargs):
        survivor = create_survivor_object(request.data)
        serializer = self.serializer_class(data=survivor)
        if not 'resources' in request.data or len(request.data['resources']) == 0:
            return Response(data={'detail': 'Informe os recursos do sobrevivente.'}, status=status.HTTP_400_BAD_REQUEST)
        if(serializer.is_valid()):
            serializer.save()
            resources = save_resources(request.data['resources'], serializer.data['id'])
            if not resources:
                response = Response(data=serializer.data, status=status.HTTP_201_CREATED)
                return response
        return Response(data={'detail': serializer.errors['detail'][0]}, status=status.HTTP_400_BAD_REQUEST)


class UpdateSurvivorLocal(UpdateAPIView):
    serializer_class = UpdateLocalSerializer

    def get_queryset(self):
        return Survivor.objects.filter(id=self.kwargs['pk'])


class ListSurvivorResources(RetrieveAPIView):
    serializer_class = ResourceSerializer
    queryset = Resource.objects.all()
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        if Survivor.objects.filter(id=kwargs['pk']).exists():
            if Survivor.objects.filter(id=kwargs['pk']).first().infected:
                return Response(data={'detail': 'Sobrevivente infectado, recursos indisponíveis.'}, status=status.HTTP_200_OK)
            resources = self.queryset.filter(survivor=kwargs['pk'])
            serializer = self.serializer_class(instance=resources, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(data={'detail': 'Sobrevivente não encontrado.'}, status=status.HTTP_404_NOT_FOUND)


class SurvivorInfected(CreateAPIView):
    serializer_class = InfectedSerializer
    queryset = Infected.objects.all()

    def create(self, request, *args, **kwargs):
        infected = request.data['infected']
        serializer = self.serializer_class(data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            return Response(data={'detail': f'Sobrevivente {infected} ralatado como infectado'}, status=status.HTTP_201_CREATED)
        return Response(data={'detail': serializer.errors['detail'][0]}, status=status.HTTP_400_BAD_REQUEST)
