from rest_framework import serializers
from .models import *

class AnalysisStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = pipe_work_state
        fields = '__all__'
        
class ImageAttributesSerializer(serializers.ModelSerializer):
    class Meta:
        model = image_attributes
        fields = '__all__'
