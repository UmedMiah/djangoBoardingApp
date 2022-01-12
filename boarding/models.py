from django.db import models
from django.contrib.auth.models import User

# These are the models, which are a mapped to tables in the postgres DB


class Products(models.Model):
    name = models.CharField(max_length=100)


class UserAccess(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
