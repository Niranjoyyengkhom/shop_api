from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=50)
    Description = models.CharField(max_length=200)
    Product_Category = models.CharField(max_length=20)
    Image_url = models.CharField(max_length=800)
    Price = models.IntegerField()
    SKU = models.CharField(max_length=20)
    Slug = models.CharField(max_length=10)


    def __str__(self):
        return self.name
