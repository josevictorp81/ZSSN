from resources.serializers import ResourceSerializer

def save_resources(resources: list, survivor_id: int) -> bool:
    """ save resources on create survivor """
    for resource in resources:
        resource['survivor'] = survivor_id
        serializer = ResourceSerializer(data=resource)
        if(serializer.is_valid()):
            serializer.save()
        else:
            return False
        