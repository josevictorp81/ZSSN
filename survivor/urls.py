from django.urls import path

from . import views

urlpatterns = [
    path('survivors', views.SurvivorCreate.as_view(), name='create-survivor'),
    path('survivors/<int:pk>/update-local', views.UpdateSurvivorLocal.as_view(), name='update-local'),
    path('resources/<int:pk>', views.ListResources.as_view(), name='list-resources'),
]