from core.models import Survivor


def get_survivor_amount() -> int:
    return Survivor.objects.filter(infected=False).count()
