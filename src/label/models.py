from django.db import models
from django_db_views.db_view import DBView
from django.db.models import CASCADE, Model

# Create your models here.
class maincategory(Model):
    name = models.CharField(max_length=20, verbose_name="Main Category", unique=True)

class attributes_type(Model):
    main = models.ForeignKey(to="maincategory", on_delete=CASCADE, verbose_name="Main Category ID")
    name = models.CharField(max_length=20, verbose_name="Type")
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["main", "name"],
                name = "unique type"
            )
        ]

class attributes(Model):
    type = models.ForeignKey(to="attributes_type", on_delete=CASCADE, verbose_name="Type")
    index = models.PositiveSmallIntegerField()
    name = models.CharField(max_length=30, verbose_name="Attributes")
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["type", "name"],
                name = "unique attribute"
            )
        ]
class color(Model):
    R = models.PositiveSmallIntegerField(verbose_name="Red Space Value")
    G = models.PositiveSmallIntegerField(verbose_name="Green Space Value")
    B = models.PositiveSmallIntegerField(verbose_name="Blue Space Value")
    persent = models.DecimalField(max_digits=3, decimal_places=1, verbose_name="Persent")
    
class attributes_color(Model):
    type = models.ForeignKey(to="attributes_type", on_delete=CASCADE, verbose_name="Type")
    color = models.ForeignKey(to="color", on_delete=CASCADE, verbose_name="Color")