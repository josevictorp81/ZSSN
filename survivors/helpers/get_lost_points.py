from core.models import Resource, Survivor

def get_points(id: int) -> int:
    """ calculate number points of each resource """
    resources = Resource.objects.filter(survivor=id)
    water_quantity = resources.get(name='Água').quantity
    medication_quantity = resources.get(name='Medicação').quantity
    food_quantity = resources.get(name='Alimentação').quantity
    ammunation_quantity = resources.get(name='Munição').quantity
    points =( water_quantity * 4) + (medication_quantity * 2) + (food_quantity * 3) + (ammunation_quantity * 1)
    return points


def get_lost_points(id: int) -> int:
    """ return number points of all resources an survivor """
    infected = Survivor.objects.get(id=id)
    return get_points(infected.id)
    