# django base
from django.shortcuts import render
from rest_framework import viewsets

# add our project
from .serializers import *


# Create your views here.
class RequestImageViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = request_image.objects.all()
    serializer_class = RequestImageSerializer
    
