from django.db import models
from django.contrib.auth.models import User
from seller.models import Product
# Create your models here.
class Cart(models.Model):
    uid = models.ForeignKey(User, on_delete=models.CASCADE, db_column="uid")
    pid = models.ForeignKey(Product, on_delete=models.CASCADE, db_column="pid")
    quantity = models.IntegerField(default=1)