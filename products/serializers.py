from .models import Catalog, FoodCategory, Brand, Product, ProductImage, CarouselItem, Review, Favorite, Cart
from django.contrib.auth import get_user_model
from rest_framework import serializers


User = get_user_model()


class CatalogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Catalog
        fields = '__all__'


class FoodCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodCategory
        fields = '__all__'


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('id', 'user', )

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user_name'] = User.objects.get(id=representation['user']).name
        return representation


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        representation['catalog_name'] = Catalog.objects.get(id=representation['catalog']).name
        representation['food_category_name'] = FoodCategory.objects.get(id=representation['food_category']).name
        representation['brand_name'] = Brand.objects.get(id=representation['brand']).name
        representation['in_favorite'] = True if Favorite.objects.filter(product=instance).exists else False
        representation['reviews'] = ReviewSerializer(instance.reviews.filter(product_id=instance.id), many=True).data

        return representation


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = '__all__'
        read_only_fields = ('users', )


class CarouselItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarouselItem
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ('id', 'user', 'product', 'created_at', 'count', )
        read_only_fields = ('id', 'users')

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

    

