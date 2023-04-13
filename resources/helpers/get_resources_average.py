from core.models import Resource, Survivor


def resource_average(resource_name: str, survivor_amount: int) -> float:
    """ reuturn all avarage resources of survivors not infected  """
    all_resources = Resource.objects.filter(name=resource_name, survivor__infected=False)
    quantity = 0
    for resource in all_resources:
        quantity += resource.quantity
    mean = quantity / survivor_amount
    return mean
