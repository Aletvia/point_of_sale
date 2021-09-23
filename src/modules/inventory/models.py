from django.db import models

"""
Model which represent a product (p. ej. Coca-Cola 500ml, 800.00, 500).
"""
class Products(models.Model):
    description = models.TextField(max_length=100)
    #unit_price = models.DecimalField(max_digits=7, decimal_places=2)
    unit_price = models.IntegerField()
    stock = models.IntegerField()