from django.db import models
from django_db_views.db_view import DBView
from django.db.models import CASCADE, Model, F

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
    data = models.JSONField(default=dict, verbose_name="Data JSON")
    #
    # class{ "type":"class", "class":"T-Shirt","index":1,  }
    # color{ "type":"color", "color":[200, 15, 170], "persent":40 }

class AttributeTable(DBView):
    # id =  models.OneToOneField(to="Attributes", primary_key=True, on_delete=models.DO_NOTHING, verbose_name="Attributes ID")
    maincategory = models.CharField(max_length=20, verbose_name="Main Category")
    attributes = models.CharField(max_length=20, verbose_name="Attributes")
    data = models.JSONField(default=dict, verbose_name="Data JSON")
    view_definition = lambda: str(
        Attributes.objects.select_related(
            "type","type__main"
            ).values(
                "id", 
                "type__main__name", 
                "type__name", 
                "data"
                ).annotate(
                    maincategory=F("type__main__name"), 
                    attributes=F("type__name")
                    ).all().query
    )
    class Meta:
        managed = False 
        db_table = "AttributeTable"