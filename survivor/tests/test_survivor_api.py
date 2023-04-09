from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from core.models import Survivor, Resource

SURVIVOR_URL = reverse('create-survivor')
INFECTED_URL = reverse('survivor-infected')

def create_survivor() -> list:
    survivors = []
    for i in range(4):
        survivor = Survivor.objects.create(name=f'name{i}', age=23, sex= 'M', local= f'12.0000{i}, 14.0000{i + 1}')
        survivors.append(survivor)
    return survivors


def resource_survivor_url(survivor_id) -> str:
    return reverse('list-resources', args=[survivor_id])


def update_url(survivor_id: int) -> str:
    return reverse('update-local', args=[survivor_id])


class SurvivorApiTest(APITestCase):
    def test_create_survivor_and_resources(self):
        data = {'name': 'name 1', 'age': 23, 'sex': 'M', 'local': '12.34563, 14.53467', 'resources': [{'name': 'agua', 'quantity': 1}, {'name': 'remedio', 'quantity': 3}]}
        
        res = self.client.post(SURVIVOR_URL, data, format='json')
        survivor = Survivor.objects.filter(id=res.data['id'])
        resource = Resource.objects.filter(survivor__id=res.data['id'])

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(resource.count(), 2)
        self.assertTrue(survivor.exists())
    
    def test_update_local(self):
        data = {'name': 'name 1', 'age': 23, 'sex': 'M', 'local': '12.00000, 14.00000'}
        survivor = Survivor.objects.create(**data)
        payload = {'local': '12.34563, 14.53467'}
        
        url = update_url(survivor_id=survivor.id)
        res = self.client.put(url, payload, format='json')

        survivor.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(survivor.local, payload['local'])
    
    def test_list_resources_of_an_survivor(self):
        data = {'name': 'name 1', 'age': 23, 'sex': 'M', 'local': '12.00000, 14.00000'}
        survivor = Survivor.objects.create(**data)
        data_resource = [{'name': 'agua', 'quantity': 1}, {'name': 'remedio', 'quantity': 3}]
        for resource in data_resource:
            Resource.objects.create(survivor=survivor, **resource)

        url = resource_survivor_url(survivor_id=survivor.id)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)
    
    def test_survivor_infected(self):
        survivors = create_survivor()
        s4 = survivors.pop()

        for survivor in survivors:
            self.client.post(INFECTED_URL, {'reporter': survivor.id, 'infected': s4.id}, format='json')
        
        infected = Survivor.objects.get(id=s4.id)

        self.assertTrue(infected.infected)

