from django.db import models

# Create your models here.
class Product(models.Model):
    product_name=models.CharField(max_length=70)
    product_description=models.TextField()
    product_price=models.PositiveIntegerField()

    def __str__(self):
        return self.product_name

