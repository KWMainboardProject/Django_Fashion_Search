from django.db import models
from django_db_views.db_view import DBView
from django.db.models import CASCADE, Model, F

from label.models import Maincategory, Attributes
from image.models import request_image
from fashion_api.settings import BASE_DIR, MEDIA_ROOT

# Create your models here.
# class pipe_work_state(Model):
#     WORK_STATE = [
#         ('U', "Undefine"),
#         ('A', "Progress"),
#         ('N', "None"),
#         ('D', "Done"),
#     ]
#     main = models.ForeignKey(to="label.Maincategory", on_delete=CASCADE, verbose_name="Main Category")
#     image = models.ForeignKey(to="image.request_image", on_delete=CASCADE, verbose_name="Image")
#     subcategory = models.CharField(max_length=1, choices=WORK_STATE, verbose_name="Sub Category Work State", default="U")
#     pattern = models.CharField(max_length=1, choices=WORK_STATE, verbose_name="Pattern Work State", default="U")
#     maincolor = models.CharField(max_length=1, choices=WORK_STATE, verbose_name="Main Color Work State", default="U")
#     subcolor = models.CharField(max_length=1, choices=WORK_STATE, verbose_name="Sub Color Work State", default="U")
    
class image_attributes(Model):
    image = models.ForeignKey(to="image.request_image", on_delete=CASCADE, verbose_name="Image")
    attribute = models.ForeignKey(to="label.Attributes", on_delete=CASCADE, verbose_name="Attributes")
    obj_idx = models.PositiveSmallIntegerField(verbose_name="Attributes")


class ImageAttributesTable(DBView):
    # id =  models.ForeignKey(to="analysis.image_attributes", primary_key=True, on_delete=models.DO_NOTHING, verbose_name="Image ID")
    image = models.ForeignKey(to="image.request_image", on_delete=CASCADE, verbose_name="Image")
    img_url = models.ImageField(verbose_name="Image URL")
    maincategory = models.ForeignKey(to="label.Maincategory", on_delete=models.DO_NOTHING, verbose_name="Main Category ID")
    attributes = models.ForeignKey(to="label.Attributes", on_delete=models.DO_NOTHING, verbose_name="Attributes ID")
    attributes_type = models.CharField(max_length=20, verbose_name="Attributes Type")
    data = models.JSONField(default=dict, verbose_name="Data JSON")
    view_definition = lambda: str(
        image_attributes.objects.select_related(
            "image", "attribute","attribute__type","attribute__type__main"
            ).values(
                "id",
                "image_id",
                "image__img",
                "attribute__type__main_id",
                "attribute_id",
                "attribute__type__name",
                "attribute__data"
                ).annotate(
                    # id=F("id"),
                    img_url=F("image__img"),
                    maincategory_id=F("attribute__type__main_id"), 
                    attributes_id=F("attribute_id"),
                    attributes_type=F("attribute__type__name"),
                    data=F("attribute__data")
                    ).all().query
    )
    class Meta:
        managed = False 
        db_table = "ImageAttributesTable"