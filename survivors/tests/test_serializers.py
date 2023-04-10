from rest_framework.test import APITestCase
from django.urls import reverse

from ..serializers import SurvivorSerializer

SURVIVOR_URL = reverse('create-survivor')

class SerializerTest(APITestCase):
    """ test serializer """
    def test_survivor_serializer(self):
        """ test create survivor """
        data = {'name': 'name 1', 'age': 23, 'sex': 'M', 'local': '12.34563, 14.53467', 'resources': [{'name': 'agua', 'quantity': 1}, {'name': 'remedio', 'quantity': 3}]}
        serializer = SurvivorSerializer(data=data).is_valid(raise_exception=True)

        self.assertTrue(serializer)
