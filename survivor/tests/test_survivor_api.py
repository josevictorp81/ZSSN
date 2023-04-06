from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from core.models import Survivor, Resource

SURVIVOR_URL = reverse('create-survivor')

def update_url(survivor_id: int)-> str:
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
