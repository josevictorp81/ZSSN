from django.urls import path

from . import views

urlpatterns = [
    path('survivors/', views.SurvivorCreate.as_view(), name='create-survivor'),
    path('survivors/<int:pk>/update-local/', views.UpdateSurvivorLocal.as_view(), name='update-local'),
    path('survivors/infected/', views.SurvivorInfected.as_view(), name='survivor-infected'),
    path('survivors/percentage-infected/', views.SurvivorInfectedPercentage.as_view(), name='percentage-infected'),
    path('survivors/percentage-not-infected/', views.SurvivorNotInfectedPercentage.as_view(), name='percentage-not-infected'),
    path('survivors/<int:pk>/lost-points/', views.LostPointsPerInfected.as_view(), name='lost-points'),
]