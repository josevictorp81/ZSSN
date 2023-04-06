from django.urls import path

from . import views

urlpatterns = [
    path('survivors', views.SurvivorCreate.as_view(), name='create-survivor'),
]