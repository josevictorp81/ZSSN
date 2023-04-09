from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from core.models import Survivor, Resource

MEAN_AMOUNT_URL = reverse('mean-amount-resources')

def resource_survivor_url(survivor_id) -> str:
    return reverse('list-resources', args=[survivor_id])


class ResourceTests(APITestCase):
    def test_list_resources_of_an_survivor(self):
        survivor = Survivor.objects.create(name='name1', age=23, sex= 'F', local= '12.00001, 14.00002')
        data_resource = [{'name': 'Água', 'quantity': 1}, {'name': 'Medicação', 'quantity': 3}]
        for resource in data_resource:
            Resource.objects.create(survivor=survivor, **resource)

        url = resource_survivor_url(survivor_id=survivor.id)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)

    def test_list_resources_of_survivor_infected(self):
        survivor = Survivor.objects.create(name='name1', age=23, sex= 'F', local= '12.00001, 14.00002', infected=True)
        data_resource = [{'name': 'Água', 'quantity': 1}, {'name': 'Medicação', 'quantity': 3}]
        for resource in data_resource:
            Resource.objects.create(survivor=survivor, **resource)

        url = resource_survivor_url(survivor_id=survivor.id)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['detail'], 'Sobrevivente infectado, recursos indisponíveis.')
    
    def test_mean_amount_resources_for_survivor(self):
        survivor1 = Survivor.objects.create(name='name1', age=23, sex= 'F', local= '12.00001, 14.00002')
        survivor2 = Survivor.objects.create(name='name2', age=25, sex= 'M', local= '12.00003, 14.00004')
        data_resource1 = [{'name': 'Água', 'quantity': 3}, {'name': 'Medicação', 'quantity': 3}, {'name': 'Alimentação', 'quantity': 5}, {'name': 'Munição', 'quantity': 1}]
        data_resource2 = [{'name': 'Água', 'quantity': 1}, {'name': 'Medicação', 'quantity': 2}, {'name': 'Alimentação', 'quantity': 3}, {'name': 'Munição', 'quantity': 1}]
        for resource in data_resource1:
            Resource.objects.create(survivor=survivor1, **resource)
        for resource in data_resource2:
            Resource.objects.create(survivor=survivor2, **resource)

        
        res = self.client.get(MEAN_AMOUNT_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['água'], 2.0)
        self.assertEqual(res.data['medicação'], 2.5)
        self.assertEqual(res.data['alimentação'], 4.0)
        self.assertEqual(res.data['munição'], 1.0)
