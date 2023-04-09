from rest_framework.test import APITestCase

from core.models import Survivor, Resource 
from ..helpers.get_resources_average import mean_water, mean_medication, mean_food, mean_ammunition

class AverageHelperTests(APITestCase):
    def test_mean_water(self):
        survivor1 = Survivor.objects.create(name='name1', age=23, sex= 'F', local= '12.00001, 14.00002')
        survivor2 = Survivor.objects.create(name='name2', age=25, sex= 'M', local= '12.00003, 14.00004')
        data_resource1 = [{'name': 'Água', 'quantity': 3}]
        data_resource2 = [{'name': 'Água', 'quantity': 1}]
        for resource in data_resource1:
            Resource.objects.create(survivor=survivor1, **resource)
        for resource in data_resource2:
            Resource.objects.create(survivor=survivor2, **resource)

        mean = mean_water()

        self.assertEqual(mean, 2.0)

    def test_mean_medication(self):
        survivor1 = Survivor.objects.create(name='name1', age=23, sex= 'F', local= '12.00001, 14.00002')
        survivor2 = Survivor.objects.create(name='name2', age=25, sex= 'M', local= '12.00003, 14.00004')
        data_resource1 = [{'name': 'Medicação', 'quantity': 3}]
        data_resource2 = [{'name': 'Medicação', 'quantity': 2}]
        for resource in data_resource1:
            Resource.objects.create(survivor=survivor1, **resource)
        for resource in data_resource2:
            Resource.objects.create(survivor=survivor2, **resource)

        mean = mean_medication()

        self.assertEqual(mean, 2.5)

    def test_mean_food(self):
        survivor1 = Survivor.objects.create(name='name1', age=23, sex= 'F', local= '12.00001, 14.00002')
        survivor2 = Survivor.objects.create(name='name2', age=25, sex= 'M', local= '12.00003, 14.00004')
        data_resource1 = [{'name': 'Alimentação', 'quantity': 5}]
        data_resource2 = [{'name': 'Alimentação', 'quantity': 3}]
        for resource in data_resource1:
            Resource.objects.create(survivor=survivor1, **resource)
        for resource in data_resource2:
            Resource.objects.create(survivor=survivor2, **resource)

        mean = mean_food()

        self.assertEqual(mean, 4.0)

    def test_mean_ammunition(self):
        survivor1 = Survivor.objects.create(name='name1', age=23, sex= 'F', local= '12.00001, 14.00002')
        survivor2 = Survivor.objects.create(name='name2', age=25, sex= 'M', local= '12.00003, 14.00004')
        data_resource1 = [{'name': 'Munição', 'quantity': 1}]
        data_resource2 = [{'name': 'Munição', 'quantity': 1}]
        for resource in data_resource1:
            Resource.objects.create(survivor=survivor1, **resource)
        for resource in data_resource2:
            Resource.objects.create(survivor=survivor2, **resource)

        mean = mean_ammunition()

        self.assertEqual(mean, 1.0)
