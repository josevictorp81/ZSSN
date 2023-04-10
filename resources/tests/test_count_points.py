from rest_framework.test import APITestCase

from ..helpers.count_points import count_resources_points

class AverageHelperTests(APITestCase):
    def test_count_points(self):
        data = [{'name': 'Água', 'quantity': 1}, {'name': 'Medicação', 'quantity': 2}, {'name': 'Alimentação', 'quantity': 1}, {'name': 'Munição', 'quantity': 1}]

        points = count_resources_points(data)

        self.assertEqual(points, 12)
