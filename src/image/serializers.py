from rest_framework import serializers
from .models import *

class RequestImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = request_image
        fields = '__all__'
