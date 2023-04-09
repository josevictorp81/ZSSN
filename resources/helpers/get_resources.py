from core.models import Resource, Survivor

def mean_water() -> float:
    surivor_amount = Survivor.objects.all().count()
    all_water = Resource.objects.filter(name='Água')
    quantity = 0
    for water in all_water:
        quantity += water.quantity
    mean = quantity / surivor_amount
    return mean


def mean_medication() -> float:
    surivor_amount = Survivor.objects.all().count()
    all_medication = Resource.objects.filter(name='Medicação')
    quantity = 0
    for medication in all_medication:
        quantity += medication.quantity
    mean = quantity / surivor_amount
    return mean


def mean_food() -> float:
    surivor_amount = Survivor.objects.all().count()
    all_food= Resource.objects.filter(name='Alimentação')
    quantity = 0
    for food in all_food:
        quantity += food.quantity
    mean = quantity / surivor_amount
    return mean


def mean_ammunition() -> float:
    surivor_amount = Survivor.objects.all().count()
    all_ammunition = Resource.objects.filter(name='Munição')
    quantity = 0
    for ammunition in all_ammunition:
        quantity += ammunition.quantity
    mean = quantity / surivor_amount
    return mean
