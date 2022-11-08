from contextlib import nullcontext
from tabnanny import verbose
from django.db import models
from account.models import User

# Create your models here.

#ManyToOne: ForeignKey
#OneToMany: ForeignKey
#둘다 many쪽에서 foreignkey(one쪽 객체) 선언하여 사용
#상품특징(OneToMany -> ForeignKey) => Attribute에서 description foreignkey로 불러오기


class Description(models.Model):
    #상품명
    productName = models.CharField(max_length=50)
    #상품상세내용
    productMemo = models.TextField()
    #상품가격
    price = models.IntegerField()

    class Meta:
        db_table = 'description'

class Product(models.Model):
    #description(OneToOne)
    description = models.OneToOneField(
        to=Description,
        on_delete = models.CASCADE,
    )
    #판매자(ManyToOne)
    seller = models.ForeignKey(
        to = "account.User",
        on_delete = models.CASCADE,
    )

    class Meta:
        db_table = 'product'


class Image(models.Model):
    #이미지가 해당되는 상품(ManyToOne)
    product = models.ForeignKey(
        to = Product,
        on_delete = models.CASCADE,
    )
    #상품이미지
    image = models.ImageField()
    #이미지 종류: 썸네일(true), 일반(false) -> default=일반(false))
    isThumbnail = models.BooleanField(default=False)
    #이미지 분석 상태 (Undefined, Progress, None, Done)

    class Meta:
        db_table = 'image'

class ProductAttributes(models.Model):
    product = models.ForeignKey(to="Product", on_delete=models.CASCADE, verbose_name="Product ID")
    attribute = models.ForeignKey(to="label.Attributes", on_delete=models.CASCADE, verbose_name="Attributes ID")
