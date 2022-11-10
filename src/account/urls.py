from django.contrib import admin
from django.urls import path, include
from rest_framework import urls, routers
from account import views

urlpatterns = [
    path('signup/', views.UserCreate.as_view()),
    path('list/', views.UserList.as_view()),
    path('api-auth/', include("rest_framework.urls")),
]