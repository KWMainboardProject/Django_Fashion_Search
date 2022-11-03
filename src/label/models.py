from django.db import models
from django.db.models import CASCADE, Model

# Create your models here.
class Maincategory(Model):
    name = models.CharField(max_length=20, verbose_name="Main Category", unique=True)

class AttributesType(Model):
    main = models.ForeignKey(to="Maincategory", on_delete=CASCADE, verbose_name="Main Category ID")
    name = models.CharField(max_length=20, verbose_name="Type")
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["main", "name"],
                name = "unique type"
            )
        ]

class Attributes(Model):
    type = models.ForeignKey(to="AttributesType", on_delete=CASCADE, verbose_name="Type")
    index = models.PositiveSmallIntegerField()
    name = models.CharField(max_length=30, verbose_name="Attributes")
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["type", "name"],
                name = "unique attribute"
            )
        ]

    
class AttributesColor(Model):
    type = models.ForeignKey(to="AttributesType", on_delete=CASCADE, verbose_name="Type")
    color = models.JSONField(default=dict, verbose_name="COLOR JSON")
    # ex {"red":150, "blue":200, "green": 30, "persent":40}