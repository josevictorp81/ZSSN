from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from core.models import Survivor, Resource

MEAN_AMOUNT_URL = reverse('mean-amount-resources')
NEGOTIATION_URL = reverse('negotiate-resources')

def resource_survivor_url(survivor_id) -> str:
    return reverse('list-resources', args=[survivor_id])

def create_survivor() -> list:
    survivor1 = Survivor.objects.create(name='name1', age=23, sex= 'F', local= '12.00001, 14.00002')
    survivor2 = Survivor.objects.create(name='name2', age=25, sex= 'M', local= '12.00003, 14.00004')
    return survivor1, survivor2


class ResourceTests(APITestCase):
    def test_list_resources_of_an_survivor(self):
        """ test list resources of an survivor """
        survivor, _ = create_survivor()
        data_resource = [{'name': 'Água', 'quantity': 1}, {'name': 'Medicação', 'quantity': 3}]
        for resource in data_resource:
            Resource.objects.create(survivor=survivor, **resource)

        url = resource_survivor_url(survivor_id=survivor.id)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)

    def test_list_resources_of_survivor_infected(self):
        """ test return resources unavailable if survivor is infected """
        survivor = Survivor.objects.create(name='name1', age=23, sex= 'F', local= '12.00001, 14.00002', infected=True)
        data_resource = [{'name': 'Água', 'quantity': 1}, {'name': 'Medicação', 'quantity': 3}]
        for resource in data_resource:
            Resource.objects.create(survivor=survivor, **resource)

        url = resource_survivor_url(survivor_id=survivor.id)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['detail'], 'Sobrevivente infectado, recursos indisponíveis.')
    
    def test_mean_amount_resources_for_survivor(self):
        """ test return average amount for each resource per survivor not infected """
        survivor1, survivor2 = create_survivor()
        survivor1.infected = True
        survivor1.save()
        data_resource1 = [{'name': 'Água', 'quantity': 3}, {'name': 'Medicação', 'quantity': 3}, {'name': 'Alimentação', 'quantity': 5}, {'name': 'Munição', 'quantity': 1}]
        data_resource2 = [{'name': 'Água', 'quantity': 1}, {'name': 'Medicação', 'quantity': 2}, {'name': 'Alimentação', 'quantity': 3}, {'name': 'Munição', 'quantity': 1}]
        for resource in data_resource1:
            Resource.objects.create(survivor=survivor1, **resource)
        for resource in data_resource2:
            Resource.objects.create(survivor=survivor2, **resource)

        
        res = self.client.get(MEAN_AMOUNT_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['Água'], 1.0)
        self.assertEqual(res.data['Medicação'], 2.0)
        self.assertEqual(res.data['Alimentação'], 3.0)
        self.assertEqual(res.data['Munição'], 1.0)
    
    def test_make_negotiation(self):
        """ test make a negotiation with success """
        survivor1, survivor2 = create_survivor()
        data_resource1 = [{'name': 'Água', 'quantity': 10}, {'name': 'Medicação', 'quantity': 20}, {'name': 'Alimentação', 'quantity': 1}, {'name': 'Munição', 'quantity': 0}]
        data_resource2 = [{'name': 'Água', 'quantity': 1}, {'name': 'Medicação', 'quantity': 5}, {'name': 'Alimentação', 'quantity': 12}, {'name': 'Munição', 'quantity': 30}]
        for resource in data_resource1:
            Resource.objects.create(survivor=survivor1, **resource)
        for resource in data_resource2:
            Resource.objects.create(survivor=survivor2, **resource)

        s1_negotiation = [{'name': 'Água', 'quantity': 3}, {'name': 'Medicação', 'quantity': 5}, {'name': 'Alimentação', 'quantity': 0}, {'name': 'Munição', 'quantity': 0}]
        s2_negotiation = [{'name': 'Água', 'quantity': 0}, {'name': 'Medicação', 'quantity': 0}, {'name': 'Alimentação', 'quantity': 4}, {'name': 'Munição', 'quantity': 10}]
        payload = {'negotiator': survivor1.id, 'target': survivor2.id, 'negotiator_resources': s1_negotiation, 'target_resources': s2_negotiation}

        res = self.client.post(NEGOTIATION_URL, payload, format='json')
        resources1 = Resource.objects.filter(survivor=survivor1.id)
        
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(resources1.get(name='Água').quantity, 7)
        self.assertEqual(resources1.get(name='Medicação').quantity, 15)
        self.assertEqual(resources1.get(name='Alimentação').quantity, 5)
        self.assertEqual(resources1.get(name='Munição').quantity, 10)
        self.assertEqual(res.data['detail'], 'Negociação realizada com sucesso.')
