from django.db import models


class Item(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    name = models.TextField()
    title = models.TextField()
    description = models.TextField()
    price = models.IntegerField()
    pv = models.IntegerField(default=0)
    status = models.BooleanField()

    def __str__(self) -> str:
        return f'{self.name}'
