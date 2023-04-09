from core.models import Resource, Survivor

def get_quantity(resources) -> int:
    quantity = 0
    for resource in resources:
        quantity += resource.quantity
    return quantity


def get_points(id: int) -> int:
    resources = Resource.objects.filter(survivor=id)
    water_quantity = get_quantity(resources.filter(name='Água'))
    medication_quantity = get_quantity(resources.filter(name='Medicação'))
    food_quantity = get_quantity(resources.filter(name='Alimentação'))
    ammunation_quantity = get_quantity(resources.filter(name='Munição'))
    points =( water_quantity * 4) + (medication_quantity * 2) + (food_quantity * 3) + (ammunation_quantity * 1)
    return points


def get_lost_points(id: int) -> int:
    infected = Survivor.objects.get(id=id)
    return get_points(infected.id)
    