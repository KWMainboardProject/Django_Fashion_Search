from django.db import models
from account.models import User
from label.models import Attributes

# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=30)
    memo = models.TextField()
    price = models.IntegerField()
    seller = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    image = models.ImageField(blank=True, upload_to="images/")

"""
class Image(models.Model):
    image = models.ImageField(blank=True, upload_to="images/")
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="image"
    )
    isThumbnail = models.BooleanField(default=False)    #썸네일 이미지인지.
"""

class Connection(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    attribute = models.ForeignKey(Attributes, on_delete=models.CASCADE)