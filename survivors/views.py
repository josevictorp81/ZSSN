from rest_framework.generics import CreateAPIView, UpdateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import SurvivorSerializer, UpdateLocalSerializer, InfectedSerializer
from core.models import Survivor, Infected
from .helpers.get_lost_points import get_lost_points


class ListAllSurvivors(ListAPIView):
    serializer_class = SurvivorSerializer
    queryset = Survivor.objects.all()


class ListInfectedSurvivors(ListAPIView):
    serializer_class = SurvivorSerializer
    queryset = Survivor.objects.filter(infected=True)


class SurvivorCreate(CreateAPIView):
    """ create survivor """
    serializer_class = SurvivorSerializer
    queryset = Survivor.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            return Response(data={'data': serializer.data, 'detail': 'Sobrevivente cadastrado com sucesso.'}, status=status.HTTP_201_CREATED)
        return Response(data={'detail': serializer.errors['detail'][0]}, status=status.HTTP_400_BAD_REQUEST)


class UpdateSurvivorLocal(UpdateAPIView):
    """ update an survivor local """
    serializer_class = UpdateLocalSerializer

    def get_queryset(self):
        return Survivor.objects.filter(id=self.kwargs['pk'])


class SurvivorInfected(CreateAPIView):
    """ report an survivor as infected """
    serializer_class = InfectedSerializer
    queryset = Infected.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            return Response(data={'detail': 'Sobrevivente reportado como infectado.'}, status=status.HTTP_201_CREATED)
        return Response(data={'detail': serializer.errors['detail'][0]}, status=status.HTTP_400_BAD_REQUEST)


class SurvivorInfectedPercentage(ListAPIView):
    """ list percentage of infected survivors """
    queryset = Survivor.objects.all()
    
    def get(self, request, *args, **kwargs):
        all_survivors = self.queryset.count()
        if all_survivors == 0:
            return Response(data={'detail': 'Não existe sobreviventes cadastrados.'}, status=status.HTTP_400_BAD_REQUEST)
        infected_survivors = self.queryset.filter(infected=True).count()
        percentage = (infected_survivors / all_survivors) * 100
        return Response(data={'detail': float(f'{percentage:.2f}')}, status=status.HTTP_200_OK)


class SurvivorNotInfectedPercentage(ListAPIView):
    """ list percentage of survivors not infected """
    queryset = Survivor.objects.all()
    
    def get(self, request, *args, **kwargs):
        all_survivors = self.queryset.count()
        if all_survivors == 0:
            return Response(data={'detail': 'Não existe sobreviventes cadastrados.'}, status=status.HTTP_400_BAD_REQUEST)
        survivors_not_infected = self.queryset.filter(infected=False).count()
        percentage = (survivors_not_infected / all_survivors) * 100
        return Response(data={'detail':float(f'{percentage:.2f}')}, status=status.HTTP_200_OK)


class LostPointsPerInfected(RetrieveAPIView):
    """ list lost points of an infected survivor """
    serializer_class = None
    queryset = Survivor.objects.all()

    def get(self, request, *args, **kwargs):
        if not self.queryset.filter(id=kwargs['pk']).exists():
            return Response(data={'detail': 'Sobrevivente não existe.'}, status=status.HTTP_404_NOT_FOUND)
        if not self.queryset.get(id=kwargs['pk']).infected:
            return Response(data={'detail': 'Este sobrevivente não é infectado.'}, status=status.HTTP_400_BAD_REQUEST)
        lost_points = get_lost_points(id=kwargs['pk'])
        return Response(data={'detail': f'{lost_points} ponto(s)'}, status=status.HTTP_200_OK)
    