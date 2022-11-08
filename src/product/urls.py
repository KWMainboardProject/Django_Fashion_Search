
from django.contrib import admin
from django.urls import path, include

from rest_framework import urls, routers

from product.views import ProductViewSet

router = routers.DefaultRouter()
router.register('register', ProductViewSet)
#router.register('detail/<int:pk>', ProductDetail)

urlpatterns = [
    path("", include(router.urls)),
    #path('register/', ProductRegister.as_view()),
]