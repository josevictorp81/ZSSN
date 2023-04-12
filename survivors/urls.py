from django.urls import path

from . import views

urlpatterns = [
    path('survivors/', views.ListAllSurvivors.as_view(), name='list-survivors'),
    path('survivors/infected/', views.ListInfectedSurvivors.as_view(), name='list-infected-survivors'),
    path('survivor/', views.SurvivorCreate.as_view(), name='create-survivor'),
    path('survivor/<int:pk>/update-local/', views.UpdateSurvivorLocal.as_view(), name='update-local'),
    path('survivor/infected/', views.SurvivorInfected.as_view(), name='survivor-infected'),
    path('survivors/percentage-infected/', views.SurvivorInfectedPercentage.as_view(), name='percentage-infected'),
    path('survivors/percentage-not-infected/', views.SurvivorNotInfectedPercentage.as_view(), name='percentage-not-infected'),
    path('survivor/<int:pk>/lost-points/', views.LostPointsPerInfected.as_view(), name='lost-points'),
]