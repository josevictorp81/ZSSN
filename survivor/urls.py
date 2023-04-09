from django.urls import path

from . import views

urlpatterns = [
    path('survivors/', views.SurvivorCreate.as_view(), name='create-survivor'),
    path('survivors/<int:pk>/update-local/', views.UpdateSurvivorLocal.as_view(), name='update-local'),
    path('survivors/infected/', views.SurvivorInfected.as_view(), name='survivor-infected'),
    path('resources/<int:pk>/', views.ListSurvivorResources.as_view(), name='list-resources'),
]