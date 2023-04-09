from core.models import Survivor

def survivor_infected_verify(id: int) -> bool:
    survivor = Survivor.objects.get(id=id)
    if survivor.infected:
        return True
    return False