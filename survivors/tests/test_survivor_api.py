from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from core.models import Survivor, Resource, Infected

SURVIVOR_URL = reverse('create-survivor')
INFECTED_URL = reverse('survivor-infected')
PERCENTAGE_INFECTED = reverse('percentage-infected')
PERCENTAGE_NOT_INFECTED = reverse('percentage-not-infected')

def create_survivor() -> list:
    survivors = []
    for i in range(4):
        survivor = Survivor.objects.create(name=f'name{i}', age=23, sex= 'M', local= f'12.0000{i}, 14.0000{i + 1}')
        survivors.append(survivor)
    return survivors


def update_url(survivor_id: int) -> str:
    return reverse('update-local', args=[survivor_id])


class SurvivorApiTest(APITestCase):
    def test_create_survivor_and_resources(self):
        data = {'name': 'name 1', 'age': 23, 'sex': 'M', 'local': '12.34563, 14.53467', 'resources': [{'name': 'agua', 'quantity': 1}, {'name': 'remedio', 'quantity': 3}]}
        
        res = self.client.post(SURVIVOR_URL, data, format='json')
        survivor = Survivor.objects.filter(id=res.data['id'])
        resource = Resource.objects.filter(survivor=res.data['id'])

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
    
    def test_survivor_infected(self):
        survivors = create_survivor()
        s4 = survivors.pop()

        for survivor in survivors:
            self.client.post(INFECTED_URL, {'reporter': survivor.id, 'infected': s4.id}, format='json')
        
        infected = Survivor.objects.get(id=s4.id)

        self.assertTrue(infected.infected)
    
    def test_reporte_infected_again(self):
        survivor1 = Survivor.objects.create(name='name1', age=23, sex= 'F', local= '12.00001, 14.00002')
        survivor2 = Survivor.objects.create(name='name2', age=35, sex= 'M', local= '12.00003, 14.00004')
        Infected.objects.create(reporter=survivor1.id, infected=survivor2.id)

        res = self.client.post(INFECTED_URL, {'reporter': survivor1.id, 'infected': survivor2.id}, format='json')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['detail'], f'Sobrevivente {survivor1.id} ja reportou o sobrevivente {survivor2.id} como infectado.')
    
    def test_survivor_infected_not_report(self):
        survivor1 = Survivor.objects.create(name='name1', age=23, sex= 'F', local= '12.00001, 14.00002', infected=True)
        survivor2 = Survivor.objects.create(name='name2', age=35, sex= 'M', local= '12.00003, 14.00004')
        Infected.objects.create(reporter=survivor1.id, infected=survivor2.id)

        res = self.client.post(INFECTED_URL, {'reporter': survivor1.id, 'infected': survivor2.id}, format='json')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['detail'], 'Sobrevivente infectado não pode reportar outro sobrevivente como infectado.')
    
    def test_dont_report_yourself(self):
        survivor1 = Survivor.objects.create(name='name1', age=23, sex= 'F', local= '12.00001, 14.00002')

        res = self.client.post(INFECTED_URL, {'reporter': survivor1.id, 'infected': survivor1.id}, format='json')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['detail'], 'Sobrevivente não pode reportar a si mesmo como infectado.')

    def test_create_survivor_no_resources(self):
        data = {'name': 'name 1', 'age': 23, 'sex': 'M', 'local': '12.34563, 14.53467'}
        
        res = self.client.post(SURVIVOR_URL, data, format='json')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['detail'], 'Informe os recursos do sobrevivente.')
    
    def test_return_percentage_of_survivors_infected(self):
        survivors = create_survivor()
        s4 = survivors[3]
        s4.infected = True
        s4.save()

        res = self.client.get(PERCENTAGE_INFECTED)
        
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['detail'], '25.00%')
    
    def test_return_percentage_of_survivors_no_infected(self):
        survivors = create_survivor()
        s4 = survivors[3]
        s4.infected = True
        s4.save()

        res = self.client.get(PERCENTAGE_NOT_INFECTED)
        
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['detail'], '75.00%')
