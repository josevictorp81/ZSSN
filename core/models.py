from django.db import models

class Survivor(models.Model):
    SEX = (
        ('F', 'Feminino'),
        ('M', 'Masculino'),
    )
    name = models.CharField(max_length=150)
    age = models.IntegerField()
    sex = models.CharField(choices=SEX, max_length=1, blank=False, null=False)
    last_local = models.CharField(max_length=25)
    infected = models.BooleanField(default=False)
    count = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.name


class Resource(models.Model):
    name = models.CharField(max_length=25)
    quantity = models.IntegerField()
    survivor = models.ForeignKey(Survivor, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name
