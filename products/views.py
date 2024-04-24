import asyncio
from .utils import send_new_review
from django.shortcuts import render
from .models import (
                     Category,
                     Brand,
                     Product,
                     ProductImage,
                     CarouselItem,
                     Review,
                     Favorite,
                     Cart,
                     Order,
                     Promotion,
                     SubCategory,
                     CustomerReview
                     )
from rest_framework import viewsets, status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from .serializers import (
                          CategorySerializer,
                          BrandSerializer,
                          ProductSerializer,
                          ProductGetSerializer,
                          ProductImageSerializer,
                          CarouselItemSerializer,
                          ReviewSerializer,
                          FavoriteSerializer,
                          CartSerializer,
                          CartListSerializer,
                          OrderSerializer,
                          PromotionSerializer,
                          SubCategorySerializer,
                          CustomerReviewSerializer
                          )

from haystack.query import SearchQuerySet
from rest_framework.views import APIView

import logging
logger = logging.getLogger(__name__)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @action(methods=['get'], detail=True)
    def get_by_category(self, request, pk=None):
        categories = Category.objects.filter(catalog=pk)
        serializer = CategorySerializer(categories, many=True)
        return Response({'products': serializer.data})
    

class SubCategoryViewSet(viewsets.ModelViewSet):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer

    @action(methods=['get'], detail=True)
    def get_by_categories(self, request, pk=None):
        subcategories = self.queryset.filter(category_id=pk)
        serializer = self.get_serializer(subcategories, many=True)
        return Response(serializer.data)
    

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
        category = self.request.query_params.getlist('category', [])
        product_name = self.request.query_params.get('product_name', None)

        if min_price is not None:
            queryset = queryset.filter(price__gte=min_price)
        if max_price is not None:
            queryset = queryset.filter(price__lte=max_price)
        if brand:
            queryset = queryset.filter(brand__id__in=brand)
        if category:
            queryset = queryset.filter(category__id__in=category)
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
        openapi.Parameter('category', openapi.IN_QUERY, description='Категории (ID)', type=openapi.TYPE_NUMBER),
        openapi.Parameter('product_name', openapi.IN_QUERY, description='Название товара', type=openapi.TYPE_STRING)
    ])
    @action(methods=['get'], detail=True)
    def get_by_category(self, request, pk=None):
        products = Product.objects.filter(category=pk)
        serializer = ProductSerializer(products, many=True)

        return Response({'products': serializer.data})
    
    
    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('min_price', openapi.IN_QUERY, description='Минимальная цена', type=openapi.TYPE_NUMBER),
        openapi.Parameter('max_price', openapi.IN_QUERY, description='Максимальная цена', type=openapi.TYPE_NUMBER),
        openapi.Parameter('brand', openapi.IN_QUERY, description='Бренды (ID)', type=openapi.TYPE_NUMBER),
        openapi.Parameter('category', openapi.IN_QUERY, description='Категории питания (ID)', type=openapi.TYPE_NUMBER),
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
        openapi.Parameter('category', openapi.IN_QUERY, description='Категории питания (ID)', type=openapi.TYPE_NUMBER),
        openapi.Parameter('product_name', openapi.IN_QUERY, description='Название товара', type=openapi.TYPE_STRING)
    ])
    @action(methods=['get'], detail=False)
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
    

class ProductSearchAPIView(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('q',openapi.IN_QUERY, description='Строка поискового запроса', type=openapi.TYPE_STRING)
        ]
    )
    def get(self, request):
        query = request.query_params.get('q', '').strip()

        if not query:
            return Response({'detail': 'Параметр не предоставлен'}, status=status.HTTP_400_BAD_REQUEST)
        
        sqs = SearchQuerySet().models(Product).autocomplete(name=query)
        sqs = sqs.filter_or(brand_name=query, category_name=query)

        products = [result.object for result in sqs]
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
        
    
    

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
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        # headers = self.get_success_headers(serializer.data)

        review = serializer.instance

        product_id = request.data.get('product')
        if product_id:
            product = Product.objects.get(id=product_id)
            self.update_product_rating(product)

        date = review.created_at.strftime('%Y-%m-%d')
        time = review.created_at.strftime('%H:%M:%S')
        message = f"Новый отзыв на продукт: {review.product.name}\n\n" \
                  f"Пользователь: {review.user.name}\n" \
                  f"Email: {review.user.email}\n" \
                  f"Рейтинг: {review.rating}\n" \
                  f"Дата: {date} в {time}\n\n" \
                  f"Отзыв: {review.text}"
        
        asyncio.run(send_new_review(message))

        return response
    
    def update_product_rating(self, product):
        reviews_count = product.reviews.count()
        new_rating = 0
        for review in product.reviews.all():
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
    

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        user = self.request.user
        if self.action == 'list':
            if user.is_anonymous:
                return Order.objects.none()
            return Order.objects.filter(user=user)
        else:
            return super().get_queryset()
        
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        order = serializer.instance
        order_items = order.items.all()
        items_details = []

        for item in order_items:
            product_detail = f'{item.product.name} - Количество: {item.quantity}'
            items_details.append(product_detail)

            Cart.objects.filter(user=request.user, product=item.product).delete()

        items_text = '\n'.join(items_details)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    

class PromotionViewSet(viewsets.ModelViewSet):
    queryset = Promotion.objects.all()
    serializer_class = PromotionSerializer



class CustomerReviewViewSet(viewsets.ModelViewSet):
    queryset = CustomerReview.objects.all()
    serializer_class = CustomerReviewSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context
    
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return response