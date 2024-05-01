from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True, required=False)

    class Meta:
        model = Product
        fields = '__all__'

    def get_image_url(self, obj):
        return obj.image_url()
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if not representation.get('image'):  # Если изображение не передано, установить изображение по умолчанию
            representation['image'] = 'img/pngtree-headphones-icon-png-image_1477376.jpg'
        return representation