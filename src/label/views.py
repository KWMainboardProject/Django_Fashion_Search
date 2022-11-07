# django base
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response

# add base
import urllib.parse as uparse

# add our project
from .serializers import *

# Create your views here.
class MaincategoryViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = maincategory.objects.all()
    serializer_class = MaincategorySerializer
    
class AttributesTypeViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = attributes_type.objects.all()
    serializer_class = AttributesTypeSerializer
    
class AttributesViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = attributes.objects.all()
    serializer_class = AttributesSerializer
    
class AttributesColorViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = attributes_color.objects.all()
    serializer_class = AttributesColorSerializer