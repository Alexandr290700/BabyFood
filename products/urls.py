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
)


router = DefaultRouter()

router.register('catalog', CatalogViewSet)
router.register('food_category', FoodCategoryViewSet)
router.register('brand', BrandViewSet)
router.register('product', ProductViewSet)
router.register('product_image', ProductImageViewSet)
router.register('carousel_item', CarouselItemViewSet)
router.register('review', ReviewViewSet)
router.register('cart', CartViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('users/favorites/', FavoriteListAPIView.as_view())
]
