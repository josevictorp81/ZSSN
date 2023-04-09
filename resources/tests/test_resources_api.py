from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from core.models import Survivor, Resource

def resource_survivor_url(survivor_id) -> str:
    return reverse('list-resources', args=[survivor_id])


class ResourceTests(APITestCase):
    def test_list_resources_of_an_survivor(self):
        survivor = Survivor.objects.create(name='name1', age=23, sex= 'F', local= '12.00001, 14.00002')
        data_resource = [{'name': 'agua', 'quantity': 1}, {'name': 'remedio', 'quantity': 3}]
        for resource in data_resource:
            Resource.objects.create(survivor=survivor, **resource)

        url = resource_survivor_url(survivor_id=survivor.id)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)

    def test_list_resources_of_survivor_infected(self):
        survivor = Survivor.objects.create(name='name1', age=23, sex= 'F', local= '12.00001, 14.00002', infected=True)
        data_resource = [{'name': 'agua', 'quantity': 1}, {'name': 'remedio', 'quantity': 3}]
        for resource in data_resource:
            Resource.objects.create(survivor=survivor, **resource)

        url = resource_survivor_url(survivor_id=survivor.id)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['detail'], 'Sobrevivente infectado, recursos indisponíveis.')
