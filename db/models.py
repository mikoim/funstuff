from django.db import models
from uuid import uuid4


class Item(models.Model):
    id = models.CharField(primary_key=True, default=uuid4, max_length=255)
    name = models.TextField(blank=True)
    title = models.TextField(blank=True)
    description = models.TextField(blank=True)
    price = models.IntegerField(default=0)
    pv = models.IntegerField(default=0)
    status = models.BooleanField(default=False)

    class Meta:
        ordering = ['id']

    def __str__(self) -> str:
        return f'{self.name}'
