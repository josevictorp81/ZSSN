from core.models import Resource, Survivor


def resource_average(resource_name: str) -> float:
    """ reuturn average of all resources """
    surivor_amount = Survivor.objects.all().count()
    all_ammunition = Resource.objects.filter(name=resource_name)
    quantity = 0
    for ammunition in all_ammunition:
        quantity += ammunition.quantity
    mean = quantity / surivor_amount
    return mean
