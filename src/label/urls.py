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
from .views import MaincategoryViewSet, AttributesTypeViewSet, AttributesViewSet, AttributesTableViewSet

#define ViewSet
maincategory_list = MaincategoryViewSet.as_view({
    'get' : 'list',
})
maincategory_detail = MaincategoryViewSet.as_view({
    'get' : 'retrieve',
})

attributesType_list = AttributesTypeViewSet.as_view({
    'get' : 'list',
})
attributesType_detail = AttributesTypeViewSet.as_view({
    'get' : 'retrieve',
})

attributes_list = AttributesViewSet.as_view({
    'get' : 'list',
})
attributes_detail = AttributesViewSet.as_view({
    'get' : 'retrieve',
})

AttributesClass_list = AttributesTableViewSet.as_view({
    'get' : 'list',
})
AttributesClass_detail = AttributesTableViewSet.as_view({
    'get' : 'retrieve',
})

urlpatterns = [
    path("maincategory/", maincategory_list),
    path("maincategory/<int:id>/", maincategory_detail),
    path("attributesType/", attributesType_list),
    path("attributesType/<int:id>/", attributesType_detail),
    path("attributes/", attributes_list),
    path("attributes/<int:id>/", attributes_detail),
    path("attributes/table/", AttributesClass_list),
    path("attributes/table/<int:id>/", AttributesClass_detail),
]
