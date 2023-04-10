from core.models import Survivor

def save_survivor_infected(id: int):
    """ update survivor infected status as true """
    survivor = Survivor.objects.get(id=id)
    survivor.infected = True
    survivor.save()
    