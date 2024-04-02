from django.shortcuts import render
from .models import (Catalog,
                     FoodCategory,
                     Brand,
                     Product,
                     ProductImage,
                     CarouselItem,
                     Review,
                     Favorite,
                     Cart,
                     )
from rest_framework import viewsets, status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from .serializers import (CatalogSerializer,
                          FoodCategorySerializer,
                          BrandSerializer,
                          ProductSerializer,
                          ProductGetSerializer,
                          ProductImageSerializer,
                          CarouselItemSerializer,
                          ReviewSerializer,
                          FavoriteSerializer,
                          CartSerializer,
                          CartListSerializer
                          )


class CatalogViewSet(viewsets.ModelViewSet):
    queryset = Catalog.objects.all()
    serializer_class = CatalogSerializer


class FoodCategoryViewSet(viewsets.ModelViewSet):
    queryset = FoodCategory.objects.all()
    serializer_class = FoodCategorySerializer

    @action(methods=['get'], detail=True)
    def get_by_category(self, request, pk=None):
        food_categories = FoodCategory.objects.filter(catalog=pk)
        serializer = FoodCategorySerializer(food_categories, many=True)
        return Response({'products': serializer.data})
    

class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        min_price = self.request.query_params.get('min_price', None)
        max_price = self.request.query_params.get('max_price', None)
        brand = self.request.query_params.getlist('brand', [])
        food_category = self.request.query_params.getlist('food_category', [])
        product_name = self.request.query_params.get('product_name', None)

        if min_price is not None:
            queryset = queryset.filter(price__gte=min_price)
        if max_price is not None:
            queryset = queryset.filter(price__lte=max_price)
        if brand:
            queryset = queryset.filter(brand__id__in=brand)
        if food_category:
            queryset = queryset.filter(food_category__id__in=food_category)
        if product_name:
            queryset = queryset.filter(name=product_name)

        return queryset
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProductGetSerializer
        elif self.action == 'favorite':
            return FavoriteSerializer
        return super().get_serializer_class()
    
    
    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('min_price', openapi.IN_QUERY, description='Минимальная цена', type=openapi.TYPE_NUMBER),
        openapi.Parameter('max_price', openapi.IN_QUERY, description='Максимальная цена', type=openapi.TYPE_NUMBER),
        openapi.Parameter('brand', openapi.IN_QUERY, description='Бренды (ID)', type=openapi.TYPE_NUMBER),
        openapi.Parameter('food_category', openapi.IN_QUERY, description='Категории питания (ID)', type=openapi.TYPE_NUMBER),
        openapi.Parameter('product_name', openapi.IN_QUERY, description='Название товара', type=openapi.TYPE_STRING)
    ])
    @action(methods=['get'], detail=True)
    def get_by_food_category(self, request, pk=None):
        products = Product.objects.filter(food_category=pk)
        serializer = ProductSerializer(products, many=True)

        return Response({'products': serializer.data})
    
    
    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('min_price', openapi.IN_QUERY, description='Минимальная цена', type=openapi.TYPE_NUMBER),
        openapi.Parameter('max_price', openapi.IN_QUERY, description='Максимальная цена', type=openapi.TYPE_NUMBER),
        openapi.Parameter('brand', openapi.IN_QUERY, description='Бренды (ID)', type=openapi.TYPE_NUMBER),
        openapi.Parameter('food_category', openapi.IN_QUERY, description='Категории питания (ID)', type=openapi.TYPE_NUMBER),
        openapi.Parameter('product_name', openapi.IN_QUERY, description='Название товара', type=openapi.TYPE_STRING)
    ])
    @action(methods=['get'], detail=True)
    def get_by_brand(self, request, pk=None):
        products = Product.objects.filter(brand=pk)
        serializer = ProductSerializer(products, many=True)

        return Response({'products': serializer.data})
    
    
    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('min_price', openapi.IN_QUERY, description='Минимальная цена', type=openapi.TYPE_NUMBER),
        openapi.Parameter('max_price', openapi.IN_QUERY, description='Максимальная цена', type=openapi.TYPE_NUMBER),
        openapi.Parameter('brand', openapi.IN_QUERY, description='Бренды (ID)', type=openapi.TYPE_NUMBER),
        openapi.Parameter('food_category', openapi.IN_QUERY, description='Категории питания (ID)', type=openapi.TYPE_NUMBER),
        openapi.Parameter('product_name', openapi.IN_QUERY, description='Название товара', type=openapi.TYPE_STRING)
    ])
    @action(methods=['get'], detail=True)
    def recommended(self, request):
        recommended_products = Product.objects.order_by('-rating', '-created_at')[:50]
        serializer = self.get_serializer(recommended_products, many=True)

        return Response({'products': serializer.data})
    

    @action(methods=['POST'], detail=True)
    def favorite(self, request, pk=None):
        product = self.get_object()
        favor = Favorite.objects.filter(user=request.user, product=product)
        if favor.exists():
            favor.delete()
            favor = False
        else:
            Favorite.objects.create(user=request.user, product=product)
            favor = True

        return Response({"In Favorite": favor})
    

class ProductImageViewSet(viewsets.ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer


class CarouselItemViewSet(viewsets.ModelViewSet):
    queryset = CarouselItem.objects.all()
    serializer_class = CarouselItemSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context
    
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)

        product_id = request.data.get('product')
        if product_id:
            product = Product.objects.get(id=product_id)
            self.update_product_rating(product)

        return response
    
    def update_product_rating(self, product):
        reviews_count = product.reviews.count()
        new_rating = 0
        for review in product.review.all():
            new_rating += review.rating

        product.rating = new_rating // reviews_count
        product.save()


class FavoriteListAPIView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_anonymous:
            return Product.objects.none()
        return Product.objects.filter(favorites__user=user)
    

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context
    
    def get_serializer_class(self):
        if self.action == 'list':
            return CartListSerializer
        else:
            return super().get_serializer_class()
        
    def get_queryset(self):
        user = self.request.user
        if user.is_anonymous:
            return Cart.objects.none()
        return Cart.objects.filter(user=user)
    
    @action(methods=['POST'], detail=False)
    def clear(self, request):
        user = request.user
        if user.is_anonymous:
            return Response({'error': 'Not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
        Cart.objects.filter(user=user).delete()
        return Response({'message': 'Success'})
