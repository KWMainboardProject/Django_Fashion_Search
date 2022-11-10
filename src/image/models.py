from django.db import models
from django.db.models import CASCADE, Model

from account.models import User
from fashion_api.settings import BASE_DIR, MEDIA_ROOT

# Create your models here.
class request_image(Model):
    WORK_STATE = [
        ('U', "Undefine"),
        ('A', "Accepted"),
        ('P', "Progress"),
        ('D', "Done"),
    ]
    
    img = models.ImageField(upload_to="requsert-image/%Y/%m/%d/", verbose_name="Image")
    requester = models.ForeignKey(to="account.User", related_name='+', on_delete=models.CASCADE)
    analysis_state = models.CharField(max_length=1, choices=WORK_STATE, verbose_name="Work State", default="U")