from resources.serializers import ResourceSerializer

def save_resources(resources, survivor) -> bool:
    for resource in resources:
        resource['survivor'] = survivor
        serializer = ResourceSerializer(data=resource)
        if(serializer.is_valid()):
            serializer.save()
        else:
            return False