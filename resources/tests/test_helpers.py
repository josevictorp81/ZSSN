from rest_framework.test import APITestCase

from core.models import Survivor, Resource
from resources.helpers.get_resources import get_resources
from resources.helpers.get_resources_average import resource_average
from resources.helpers.update_negotiantion import update_resources
from resources.helpers.count_points import count_resources_points


def create_survivor() -> list:
    survivor1 = Survivor.objects.create(name='name1', age=23, sex= 'F', local= '12.00001, 14.00002')
    survivor2 = Survivor.objects.create(name='name2', age=25, sex= 'M', local= '12.00003, 14.00004')
    return survivor1, survivor2


class HelperTests(APITestCase):
    def test_count_points(self):
        """ test return number points of resounces amount """
        data = [{'name': 'Água', 'quantity': 1}, {'name': 'Medicação', 'quantity': 2}, {'name': 'Alimentação', 'quantity': 1}, {'name': 'Munição', 'quantity': 1}]

        points = count_resources_points(data)

        self.assertEqual(points, 12)

    def test_update_resources(self):
        """ test negotiation resources """
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
    
    def test_mean_water(self):
        survivor1, survivor2 = create_survivor()
        data_resource1 = [{'name': 'Água', 'quantity': 3}]
        data_resource2 = [{'name': 'Água', 'quantity': 1}]
        for resource in data_resource1:
            Resource.objects.create(survivor=survivor1, **resource)
        for resource in data_resource2:
            Resource.objects.create(survivor=survivor2, **resource)

        mean = resource_average(resource_name='Água')

        self.assertEqual(mean, 2.0)

    def test_mean_medication(self):
        survivor1, survivor2 = create_survivor()
        data_resource1 = [{'name': 'Medicação', 'quantity': 3}]
        data_resource2 = [{'name': 'Medicação', 'quantity': 2}]
        for resource in data_resource1:
            Resource.objects.create(survivor=survivor1, **resource)
        for resource in data_resource2:
            Resource.objects.create(survivor=survivor2, **resource)

        mean = resource_average(resource_name='Medicação')

        self.assertEqual(mean, 2.5)

    def test_mean_food(self):
        survivor1, survivor2 = create_survivor()
        data_resource1 = [{'name': 'Alimentação', 'quantity': 5}]
        data_resource2 = [{'name': 'Alimentação', 'quantity': 3}]
        for resource in data_resource1:
            Resource.objects.create(survivor=survivor1, **resource)
        for resource in data_resource2:
            Resource.objects.create(survivor=survivor2, **resource)

        mean = resource_average(resource_name='Alimentação')

        self.assertEqual(mean, 4.0)

    def test_mean_ammunition(self):
        survivor1, survivor2 = create_survivor()
        data_resource1 = [{'name': 'Munição', 'quantity': 1}]
        data_resource2 = [{'name': 'Munição', 'quantity': 1}]
        for resource in data_resource1:
            Resource.objects.create(survivor=survivor1, **resource)
        for resource in data_resource2:
            Resource.objects.create(survivor=survivor2, **resource)

        mean = resource_average(resource_name='Munição')

        self.assertEqual(mean, 1.0)
    
    def test_get_resources(self):
        """ test resources of an survivor """
        survivor1 = Survivor.objects.create(name='name1', age=23, sex= 'F', local= '12.00001, 14.00002')
        data_resource1 = [{'name': 'Água', 'quantity': 10}, {'name': 'Medicação', 'quantity': 20}, {'name': 'Alimentação', 'quantity': 1}, {'name': 'Munição', 'quantity': 0}]
        for resource in data_resource1:
            Resource.objects.create(survivor=survivor1, **resource)

        resources = get_resources(survivor_id=survivor1.id)

        self.assertEqual(resources.count(), 4)
        self.assertEqual(resources.get(name='Água').quantity, 10)
