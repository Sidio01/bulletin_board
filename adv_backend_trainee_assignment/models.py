import datetime
from django.db import models


class Ad(models.Model):
    """Модель объявления."""
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)
    urls_list = models.CharField(max_length=1000)
    price = models.PositiveIntegerField()
    date = models.CharField(max_length=100)
