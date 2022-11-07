from django.db import models
from django_db_views.db_view import DBView
from django.db.models import CASCADE, Model, F

from label.models import Maincategory, Attributes, AttributeIndexTable
from image.models import request_image
from analysis.models import ImageAttributesTable
from fashion_api.settings import BASE_DIR, MEDIA_ROOT

# Create your models here.
class search_request(Model):
    WORK_STATE = [
        ('U', "Undefine"),
        ('A', "Progress"),
        ('N', "None"),
        ('D', "Done"),
    ]
    
    image = models.ForeignKey(to="image.request_image", on_delete=CASCADE, verbose_name="Image")
    maincategory = models.ForeignKey(to="label.Maincategory", on_delete=CASCADE, verbose_name="Main Categtegory ID")
    state =  models.CharField(max_length=1, choices=WORK_STATE, verbose_name="Search Work State", default="U")
    
class search_result(Model):
    score = models.FloatField(verbose_name="Score")