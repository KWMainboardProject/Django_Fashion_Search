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
    queryset = Maincategory.objects.all()
    serializer_class = MaincategorySerializer
    
class AttributesTypeViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = AttributesType.objects.all()
    serializer_class = AttributesTypeSerializer
    
class AttributesViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = Attributes.objects.all()
    serializer_class = AttributesSerializer

class AttributesTableViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = AttributeTable.objects.all()
    serializer_class = AttributesTableSerializer
    
class AttributesIndexTableViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = AttributeIndexTable.objects.all()
    serializer_class = AttributesIndexTableSerializer