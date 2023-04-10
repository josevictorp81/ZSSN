from core.models import Survivor

def survivor_exists(survivor_id: int) -> bool:
    return Survivor.objects.filter(id=survivor_id).exists()
