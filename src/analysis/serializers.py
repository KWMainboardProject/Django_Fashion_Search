from rest_framework import serializers
from .models import *

class AnalysisStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = analysis_state
        fields = '__all__'
        
class ImageAttributesSerializer(serializers.ModelSerializer):
    class Meta:
        model = image_attributes
        fields = '__all__'

class ImageAttributesColortSerializer(serializers.ModelSerializer):
    class Meta:
        model = image_attributes_color
        fields = '__all__'
