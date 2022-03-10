from django.contrib.auth.models import AbstractUser
from django.db import models
from django_sharding_library.models import TableStrategyModel, ShardedByMixin


class User(models.Model):
    id = models.IntegerField(db_column='id', primary_key=True)
    name = models.CharField(db_column='name', max_length=100)
    year = models.IntegerField(db_column='year')


class Books(models.Model):
    id = models.IntegerField(db_column='id', primary_key=True)
    name = models.CharField(db_column='name', max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

