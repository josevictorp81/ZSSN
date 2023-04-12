from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from core.models import Survivor, Resource, Infected

SURVIVOR_URL = reverse('create-survivor')
INFECTED_URL = reverse('survivor-infected')
PERCENTAGE_INFECTED = reverse('percentage-infected')
PERCENTAGE_NOT_INFECTED = reverse('percentage-not-infected')
LIST_SURVIVORS_URL = reverse('list-survivors')
LIST_SURVIVORS_INFECTED_URL = reverse('list-infected-survivors')

def create_survivor() -> list:
    survivors = []
    for i in range(4):
        survivor = Survivor.objects.create(name=f'name{i}', age=23, sex= 'M', local= f'12.0000{i}, 14.0000{i + 1}')
        survivors.append(survivor)
    return survivors


def survivor_url(url: str, survivor_id) -> str:
    return reverse(url, args=[survivor_id])


class SurvivorApiTest(APITestCase):
    def test_list_survivors(self):
        """ test list all survivors """
        create_survivor()

        res = self.client.get(LIST_SURVIVORS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 4)
    
    def test_list_survivors(self):
        """ test list all infected survivors """
        suvivors = create_survivor()
        s4 = suvivors.pop()
        s4.infected = True
        s4.save()

        res = self.client.get(LIST_SURVIVORS_INFECTED_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)

    def test_create_survivor_and_resources(self):
        """ teste create survivor on success """
        data = {'name': 'name 1', 'age': 23, 'sex': 'M', 'local': '12.34563, 14.53467', 'resources': [{'name': 'agua', 'quantity': 1}, {'name': 'remedio', 'quantity': 3}]}
        
        res = self.client.post(SURVIVOR_URL, data, format='json')
        survivor = Survivor.objects.filter(id=res.data['data']['id'])
        resource = Resource.objects.filter(survivor=res.data['data']['id'])

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['detail'], 'Sobrevivente cadastrado com sucesso.')
        self.assertEqual(resource.count(), 2)
        self.assertTrue(survivor.exists())
    
    def test_create_survivor_no_resources(self):
        """ test create survivor with error, resouces are not provided """
        data = {'name': 'name 1', 'age': 23, 'sex': 'M', 'local': '12.34563, 14.53467', 'resources': []}
        
        res = self.client.post(SURVIVOR_URL, data, format='json')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['detail'], 'Informe os recursos do sobrevivente.')
    
    def test_update_local(self):
        """ test update local of an survivor """
        data = {'name': 'name 1', 'age': 23, 'sex': 'M', 'local': '12.00000, 14.00000'}
        survivor = Survivor.objects.create(**data)
        payload = {'local': '12.34563, 14.53467'}
        
        url = survivor_url(url='update-local', survivor_id=survivor.id)
        res = self.client.put(url, payload, format='json')

        survivor.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(survivor.local, payload['local'])
    
    def test_survivor_infected(self):
        """ test report survivor as infected """
        survivors = create_survivor()
        s4 = survivors.pop()

        for survivor in survivors:
            self.client.post(INFECTED_URL, {'reporter': survivor.id, 'infected': s4.id}, format='json')
        
        infected = Survivor.objects.get(id=s4.id)

        self.assertTrue(infected.infected)
    
    def test_reporte_infected_again(self):
        """ test do not report infected survivor one more time """
        survivor1 = Survivor.objects.create(name='name1', age=23, sex= 'F', local= '12.00001, 14.00002')
        survivor2 = Survivor.objects.create(name='name2', age=35, sex= 'M', local= '12.00003, 14.00004')
        Infected.objects.create(reporter=survivor1.id, infected=survivor2.id)

        res = self.client.post(INFECTED_URL, {'reporter': survivor1.id, 'infected': survivor2.id}, format='json')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['detail'], f'Sobrevivente {survivor1.id} ja reportou o sobrevivente {survivor2.id} como infectado.')
    
    def test_survivor_infected_not_report(self):
        """ test do not infected survivor report another survivor """
        survivor1 = Survivor.objects.create(name='name1', age=23, sex= 'F', local= '12.00001, 14.00002', infected=True)
        survivor2 = Survivor.objects.create(name='name2', age=35, sex= 'M', local= '12.00003, 14.00004')
        Infected.objects.create(reporter=survivor1.id, infected=survivor2.id)

        res = self.client.post(INFECTED_URL, {'reporter': survivor1.id, 'infected': survivor2.id}, format='json')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['detail'], 'Sobrevivente infectado não pode reportar outro sobrevivente como infectado.')
    
    def test_dont_report_yourself(self):
        """ test do not survivor report yourself as infected """
        survivor1 = Survivor.objects.create(name='name1', age=23, sex= 'F', local= '12.00001, 14.00002')

        res = self.client.post(INFECTED_URL, {'reporter': survivor1.id, 'infected': survivor1.id}, format='json')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['detail'], 'Sobrevivente não pode reportar a si mesmo como infectado.')
    
    def test_return_percentage_of_survivors_infected(self):
        """ test return percentage of infected survivors """
        survivors = create_survivor()
        s4 = survivors[3]
        s4.infected = True
        s4.save()

        res = self.client.get(PERCENTAGE_INFECTED)
        
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['detail'], 25.00)
    
    def test_return_percentage_of_survivors_no_infected(self):
        """ test return percentage of not infected survivors """
        survivors = create_survivor()
        s4 = survivors[3]
        s4.infected = True
        s4.save()

        res = self.client.get(PERCENTAGE_NOT_INFECTED)
        
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['detail'], 75.00)
    
    def test_lost_points(self):
        """ test return lost points of an infected survivor """
        survivor1 = Survivor.objects.create(name='name1', age=23, sex= 'F', local= '12.00001, 14.00002')
        survivor2 = Survivor.objects.create(name='name2', age=25, sex= 'M', local= '12.00003, 14.00004', infected=True)
        data_resource1 = [{'name': 'Água', 'quantity': 3}, {'name': 'Medicação', 'quantity': 3}, {'name': 'Alimentação', 'quantity': 5}, {'name': 'Munição', 'quantity': 1}]
        data_resource2 = [{'name': 'Água', 'quantity': 1}, {'name': 'Medicação', 'quantity': 2}, {'name': 'Alimentação', 'quantity': 3}, {'name': 'Munição', 'quantity': 1}]
        for resource in data_resource1:
            Resource.objects.create(survivor=survivor1, **resource)
        for resource in data_resource2:
            Resource.objects.create(survivor=survivor2, **resource)

        url = survivor_url(url='lost-points', survivor_id=survivor2.id)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['detail'], '18 ponto(s)')
