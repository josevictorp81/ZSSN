from core.models import Survivor

def survivor_exists(survivor_id: int) -> bool:
    """ return status if survivor exists or no """
    return Survivor.objects.filter(id=survivor_id).exists()
