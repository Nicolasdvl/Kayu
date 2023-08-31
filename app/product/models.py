from django.db import models

class Product(models.Model):
    code = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=250)
    brand = models.CharField(max_length=250)
    image = models.URLField()
    nutriscore = models.CharField(
        choices=[
            ('A', 'A'),
            ('B', 'B'),
            ('C', 'C'),
            ('D', 'D'),
            ('E', 'E'),
            ('N', 'Indéfini'),
            ],
        max_length=1,
        default='N'
        )
    ingredients = models.TextField()


class Category(models.Model):
    id = models.CharField(primary_key=True, max_length=250)
    name = models.CharField(max_length=250)
    products = models.ManyToManyField(Product)