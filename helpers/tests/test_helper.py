from rest_framework.test import APITestCase

from core.models import Survivor
from ..verify_survivor_exist import survivor_exists
from ..verify_survivor_infected import survivor_infected

class HelperTests(APITestCase):
    def test_survivor_exists_true(self):
        """ test return true if survivor exists """
        survivor = Survivor.objects.create(name='name1', age=23, sex= 'F', local= '12.00001, 14.00002')

        exist = survivor_exists(survivor_id=survivor.id)

        self.assertTrue(exist)
    
    def test_survivor_exists_false(self):
        """ test return true if survivor exists """
        exist = survivor_exists(survivor_id=1)

        self.assertFalse(exist)
    
    def test_survivor_infected_true(self):
        survivor = Survivor.objects.create(name='name1', age=23, sex= 'F', local= '12.00001, 14.00002', infected=True)

        infected = survivor_infected(survivor_id=survivor.id)

        self.assertTrue(infected)
    
    def test_survivor_infected_false(self):
        survivor = Survivor.objects.create(name='name1', age=23, sex= 'F', local= '12.00001, 14.00002')

        infected = survivor_infected(survivor_id=survivor.id)

        self.assertFalse(infected)