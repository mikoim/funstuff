from django.db import models


class Item(models.Model):
    name = models.TextField()
    title = models.TextField()
    description = models.TextField()
    price = models.IntegerField()
    pv = models.IntegerField()
    status = models.BooleanField()

    def __str__(self) -> str:
        return f'{self.name}'
