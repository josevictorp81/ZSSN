from core.models import Survivor

def survivor_exists(survivor: int) -> bool:
    return Survivor.objects.filter(id=survivor).exists()
