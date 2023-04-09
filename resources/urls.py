from django.urls import path

from . import views

urlpatterns = [
    path('resources/<int:pk>/', views.ListSurvivorResources.as_view(), name='list-resources'),
    path('resources/mean-amount-resources/', views.MeanAmountResources.as_view(), name='mean-amount-resources'),

]