from django.db import models
from django.contrib.auth.models import User
import datetime as dt

# Create your models here.

class List(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    title = models.CharField(max_length=100)
    last_updated = models.DateTimeField(default=dt.datetime.now())

    