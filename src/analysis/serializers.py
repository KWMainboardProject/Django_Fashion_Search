from rest_framework import serializers
from .models import *

class MaincategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = maincategory
        fields = '__all__'
        
class AttributesTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = attributes_type
        fields = '__all__'

class AttributesSerializer(serializers.ModelSerializer):
    class Meta:
        model = attributes
        fields = '__all__'
        
class AttributesColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = attributes_color
        fields = '__all__'