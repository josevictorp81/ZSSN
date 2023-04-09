from core.models import Survivor

def save_survivor_infected(id: int):
    survivor = Survivor.objects.get(id=id)
    survivor.infected = True
    survivor.save()