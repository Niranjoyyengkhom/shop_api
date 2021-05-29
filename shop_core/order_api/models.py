from django.db import models

# Create your models here.
class Order(models.Model):
        name = models.CharField(max_length=50)
        Location = models.CharField(max_length=200)
        Total_Price = models.IntegerField()
        Quantity = models.IntegerField()
        Status = models.CharField(max_length=20)