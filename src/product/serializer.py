from .models import *
from rest_framework import serializers


class ImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)
    product = serializers.ReadOnlyField(source='product.id')

    class Meta:
        model = Image
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    user = serializers.ReadOnlyField(source='user.username')

    def get_images(self, obj):
        image = obj.image.all()
        return ImageSerializer(instance=image, many=True).data

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'memo', 'images', 'user']


    def create(self, validated_data):
        #print(validated_data)
        instance = Product.objects.create(**validated_data)
        image_set = self.context['request'].FILES
        for image_data in image_set.getlist('image'):
            Image.objects.create(image=image_data, product=instance)
        return instance