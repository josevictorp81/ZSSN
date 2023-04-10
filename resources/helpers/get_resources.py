from core.models import Resource


def get_resources(survivor_id: int) -> list:
    """ return all resources of an survivor """
    return Resource.objects.filter(survivor=survivor_id)
