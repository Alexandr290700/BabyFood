from .models import (Catalog,
                    FoodCategory,
                    Brand,
                    Product,
                    ProductImage,
                    CarouselItem,
                    Review,
                    Favorite,
                    Cart,
                    Order,
                    OrderItem,
                    Promotion,
                    )
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
    food_category_name = serializers.SerializerMethodField()
    brand_name = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'

    def get_food_category_name(self, obj):
        return obj.food_category.name if obj.food_category else None
    
    def get_brand_name(self, obj):
        return obj.brand.name if obj.brand else None

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['food_category_name'] = FoodCategory.objects.get(id=representation['food_category']).name
        representation['brand_name'] = Brand.objects.get(id=representation['brand']).name

        return representation
    

class ProductGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
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


class CartListSerializer(serializers.ModelSerializer):
    product = ProductSerializer
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
    
    class Meta:
        model = Cart
        fields = '__all__'
        read_only_fields = ('id', 'user')


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ('id', 'user', 'product', 'created_at', 'count', )
        read_only_fields = ('id', 'users')

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
    

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ('id', 'user', 'name', 'phone', 'email', 'shipping_address', 'items')
        read_only_fields = ('id', 'user', )

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        validated_data['user'] = self.context['request'].user
        order = Order.objects.create(**validated_data)
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        return order
    

class PromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = '__all__'
