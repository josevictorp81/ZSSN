from core.models import Resource

def remove_resources(survivor, resources):
    """ remove resources after success negotiation """
    for resource in resources:
        res = Resource.objects.get(survivor=survivor, name=resource['name'])
        res.quantity -= resource['quantity']
        res.save()


def add_resources(survivor, resources):
    """ add resources after success negotiation """
    for resource in resources:
        res = Resource.objects.get(survivor=survivor, name=resource['name'])
        res.quantity += resource['quantity']
        res.save()
