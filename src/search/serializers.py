from rest_framework import serializers
from .models import *

class SearchRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = search_request
        fields = '__all__'
        
class SearchResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = search_result
        fields = '__all__'