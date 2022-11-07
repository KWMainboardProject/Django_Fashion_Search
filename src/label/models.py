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

    
class attributes_color(Model):
    type = models.ForeignKey(to="attributes_type", on_delete=CASCADE, verbose_name="Type")
    color = models.JSONField(default=dict, verbose_name="COLOR JSON")
    # ex {"red":150, "blue":200, "green": 30, "persent":40}