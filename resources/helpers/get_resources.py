from core.models import Resource


def get_resources(id):
    return Resource.objects.filter(survivor=id)
