from django.db import models


class Item(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    name = models.TextField(blank=True)
    title = models.TextField(blank=True)
    description = models.TextField(blank=True)
    price = models.IntegerField()
    pv = models.IntegerField()
    status = models.BooleanField()

    def __str__(self) -> str:
        return f'{self.name}'
