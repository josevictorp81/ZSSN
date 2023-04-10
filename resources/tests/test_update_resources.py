from rest_framework.test import APITestCase

from core.models import Survivor, Resource
from ..helpers.update_negotiantion import update_resources

class AverageHelperTests(APITestCase):
    def test_update_resources(self):
        survivor1 = Survivor.objects.create(name='name1', age=23, sex= 'F', local= '12.00001, 14.00002')
        survivor2 = Survivor.objects.create(name='name2', age=25, sex= 'M', local= '12.00003, 14.00004')
        data_resource1 = [{'name': 'Água', 'quantity': 10}, {'name': 'Medicação', 'quantity': 20}, {'name': 'Alimentação', 'quantity': 1}, {'name': 'Munição', 'quantity': 0}]
        data_resource2 = [{'name': 'Água', 'quantity': 1}, {'name': 'Medicação', 'quantity': 5}, {'name': 'Alimentação', 'quantity': 12}, {'name': 'Munição', 'quantity': 30}]
        for resource in data_resource1:
            Resource.objects.create(survivor=survivor1, **resource)
        for resource in data_resource2:
            Resource.objects.create(survivor=survivor2, **resource)

        s1_negotiation = [{'name': 'Água', 'quantity': 3}, {'name': 'Medicação', 'quantity': 5}]
        s2_negotiation = [{'name': 'Alimentação', 'quantity': 4}, {'name': 'Munição', 'quantity': 10}]

        update_resources(survivor=survivor1.id, resources=s1_negotiation)
        update_resources(survivor=survivor2.id, resources=s2_negotiation)
        update_resources(survivor=survivor1.id, resources=s2_negotiation)
        update_resources(survivor=survivor2.id, resources=s1_negotiation)

        resources1 = Resource.objects.filter(survivor=survivor1.id)
        self.assertEqual(resources1.get(name='Água').quantity, 7)
        self.assertEqual(resources1.get(name='Medicação').quantity, 15)
        self.assertEqual(resources1.get(name='Alimentação').quantity, 5)
        self.assertEqual(resources1.get(name='Munição').quantity, 10)
        