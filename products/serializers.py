import json
from .models import (
                    Category,
                    Brand,
                    Product,
                    ProductImage,
                    CarouselItem,
                    MobileCarouselItem,
                    Review,
                    Favorite,
                    Cart,
                    Order,
                    OrderItem,
                    Promotion,
                    SubCategory,
                    CustomerReview
                    )
from django.contrib.auth import get_user_model
from rest_framework import serializers


User = get_user_model()



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
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
    category_name = serializers.SerializerMethodField()
    brand_name = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'

    def get_category_name(self, obj):
        return obj.category.name if obj.category else None
    
    def get_brand_name(self, obj):
        return obj.brand.name if obj.brand else None

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['category_name'] = Category.objects.get(id=representation['category']).name
        representation['subcategory_title'] = SubCategory.objects.get(id=representation['subcategory']).title
        representation['brand_name'] = Brand.objects.get(id=representation['brand']).name
        extra_info_json = json.loads(instance.extra_info)
        representation['extra_info'] = extra_info_json


        return representation
    

class ProductGetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['category_name'] = Category.objects.get(id=representation['category']).name
        representation['subcategory_title'] = SubCategory.objects.get(id=representation['subcategory']).title
        representation['brand_name'] = Brand.objects.get(id=representation['brand']).name
        representation['in_favorite'] = True if Favorite.objects.filter(product=instance).exists else False
        representation['reviews'] = ReviewSerializer(instance.reviews.filter(product_id=instance.id), many=True).data
        
        product_images = ProductImage.objects.filter(product=instance)
        representation['product_images'] = [image.image.url for image in product_images]
        representation['brand_image'] = Brand.objects.get(id=representation['brand']).image.url
        extra_info_json = json.loads(instance.extra_info)
        representation['extra_info'] = extra_info_json


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


class MobileCarouselItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MobileCarouselItem
        fields = '__all__'


class CartListSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    
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
        fields = '__all__'
        read_only_fields = ('id', 'user', 'created_at')

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
        fields = fields = '__all__'
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


class CustomerReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerReview
        fields = '__all__'
        read_only_fields = ('id', 'user', )

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
    
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user_name'] = User.objects.get(id=representation['user']).name
        return representation