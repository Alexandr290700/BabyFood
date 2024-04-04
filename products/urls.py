from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CatalogViewSet,
    FoodCategoryViewSet,
    BrandViewSet,
    ProductViewSet,
    ProductImageViewSet,
    CarouselItemViewSet,
    ReviewViewSet,
    FavoriteListAPIView,
    CartViewSet,
    OrderViewSet,
    ProductSearchAPIView,
)


router = DefaultRouter()

router.register('catalogs', CatalogViewSet)
router.register('food_categories', FoodCategoryViewSet)
router.register('brands', BrandViewSet)
router.register('products', ProductViewSet)
router.register('product_images', ProductImageViewSet)
router.register('carousel_items', CarouselItemViewSet)
router.register('reviews', ReviewViewSet)
router.register('carts', CartViewSet)
router.register('orders', OrderViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('users/favorites/', FavoriteListAPIView.as_view()),
    path('search/', ProductSearchAPIView.as_view(), name='product-search'),
    # path('search/<str:query>/', ProductSearchAPIView.as_view(), name='product-search-query'),
]
