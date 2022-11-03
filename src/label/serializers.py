from rest_framework import serializers
from .models import *

class MaincategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Maincategory
        fields = '__all__'
        
class AttributesTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributesType
        fields = '__all__'

class AttributesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attributes
        fields = '__all__'
        
class AttributesTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributeTable
        fields = '__all__'