from django.db import models
from django_db_views.db_view import DBView
from django.db.models import CASCADE, Model, F

from label.models import Maincategory, Attributes, AttributeIndexTable
from image.models import request_image
from fashion_api.settings import BASE_DIR, MEDIA_ROOT

# Create your models here.
class pipe_work_state(Model):
    WORK_STATE = [
        ('U', "Undefine"),
        ('A', "Progress"),
        ('N', "None"),
        ('D', "Done"),
    ]
    main = models.ForeignKey(to="label.Maincategory", on_delete=CASCADE, verbose_name="Main Category")
    image = models.ForeignKey(to="image.request_image", on_delete=CASCADE, verbose_name="Image")
    subcategory = models.CharField(max_length=1, choices=WORK_STATE, verbose_name="Sub Category Work State", default="U")
    pattern = models.CharField(max_length=1, choices=WORK_STATE, verbose_name="Pattern Work State", default="U")
    maincolor = models.CharField(max_length=1, choices=WORK_STATE, verbose_name="Main Color Work State", default="U")
    subcolor = models.CharField(max_length=1, choices=WORK_STATE, verbose_name="Sub Color Work State", default="U")
    
class image_attributes(Model):
    image = models.ForeignKey(to="image.request_image", on_delete=CASCADE, verbose_name="Image")
    attribute = models.ForeignKey(to="label.Attributes", on_delete=CASCADE, verbose_name="Attributes")
    obj_idx = models.PositiveSmallIntegerField(verbose_name="Attributes")
