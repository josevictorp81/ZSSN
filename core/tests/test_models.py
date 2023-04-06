from django.test import TestCase

from ..models import Survivor, Resource

def create_survivor() -> Survivor:
    return Survivor.objects.create(name='survivor 1', age=23, sex='M', last_local='12.34567, 8.89744')

class ModelTests(TestCase):
    def test_create_survivor(self):
        survivor = create_survivor()

        self.assertEqual(survivor.__str__(), 'survivor 1')
    
    def test_create_resource(self):
        survivor = create_survivor()
        resource = Resource.objects.create(name='agua', quantity=1, survivor=survivor)

        self.assertEqual(resource.__str__(), 'agua')