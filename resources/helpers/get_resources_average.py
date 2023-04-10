from core.models import Resource, Survivor


def resource_average(resource_name: str, survivor_amount: int) -> float:
    """ reuturn average of all resources """
    all_resources = Resource.objects.filter(name=resource_name)
    quantity = 0
    for resource in all_resources:
        quantity += resource.quantity
    mean = quantity / survivor_amount
    return mean
