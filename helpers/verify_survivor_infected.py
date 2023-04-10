from core.models import Survivor

def survivor_infected(survivor_id: int) -> bool:
    survivor = Survivor.objects.get(id=survivor_id)
    if survivor.infected:
        return True
    return False
