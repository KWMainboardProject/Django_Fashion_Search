
from django.contrib import admin
from django.urls import path, include

from rest_framework import urls, routers

from product import views

#router = routers.DefaultRouter()
#router.register('register', ProductViewSet)
#router.register('detail/<int:pk>', ProductDetail)

urlpatterns = [
    #path("", include(router.urls)),
    path('register/', views.product_register),
    path('detail/<int:pk>/', views.product_detail),
    path('list/', views.product_list),
    path('user_product_list/', views.user_product_list),
]