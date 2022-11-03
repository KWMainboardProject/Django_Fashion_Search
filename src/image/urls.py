"""carom_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import RequestImageViewSet

#define ViewSet
image_list = RequestImageViewSet.as_view({
    'get' : 'list',
    'post' : 'create',
})
image_detail = RequestImageViewSet.as_view({
    'get' : 'retrieve',
    'put': 'update',
    'delete' : 'destroy'
})

#define url pattern
urlpatterns =[
    path('request/', image_list),
    path('request/<int:pk>/', image_detail),
]
