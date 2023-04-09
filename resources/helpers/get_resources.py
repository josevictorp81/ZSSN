from core.models import Resource, Survivor

def mean_water() -> float:
    surivor_amount = Survivor.objects.all().count()
    all_water = Resource.objects.filter(name='Água')
    quantity = 0
    for water in all_water:
        quantity += water.quantity
    mean = quantity / surivor_amount
    return mean
