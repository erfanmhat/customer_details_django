from django.db import models


# Create your models here.
class Customer(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    address = models.CharField(max_length=250)
    city = models.CharField(max_length=30)
    country = models.CharField(max_length=30)
    email = models.EmailField()
