from django.db import models
from django.contrib.auth.models import User
import datetime as dt

# Create your models here.

class List(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    title = models.CharField(max_length=100)
    last_updated = models.DateTimeField(default=dt.datetime.now())

    def __str__(self) -> str:
        return self.title


class Task(models.Model):
    list = models.ForeignKey(List, on_delete=models.CASCADE)
    task = models.TextField()

    def __str__(self) -> str:
        return str(self.list.pk)