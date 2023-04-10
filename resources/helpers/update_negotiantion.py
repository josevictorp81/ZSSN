from core.models import Resource

def update_resources(survivor, resources):
    for resource in resources:
        res = Resource.objects.get(survivor=survivor, name=resource['name'])
        if resource['quantity'] < res.quantity:
            res.quantity -= resource['quantity']
        if resource['quantity'] >= res.quantity:
            res.quantity = res.quantity + resource['quantity']
        res.save()
