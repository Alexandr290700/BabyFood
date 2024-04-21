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
    PromotionViewSet,
    BrandImageViewSet,
    ExtraInfoViewSet,
)


router = DefaultRouter()

router.register('catalogs', CatalogViewSet)
router.register('food_categories', FoodCategoryViewSet)
router.register('brands', BrandViewSet)
router.register('products', ProductViewSet)
router.register('product_images', ProductImageViewSet)
router.register('carousel_items', CarouselItemViewSet)
router.register('reviews', ReviewViewSet)
router.register(r'carts', CartViewSet)
router.register(r'orders', OrderViewSet)
router.register('promotion', PromotionViewSet)
router.register('brand_image', BrandImageViewSet)
router.register('extra_info', ExtraInfoViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('users/favorites/', FavoriteListAPIView.as_view()),
    path('search/', ProductSearchAPIView.as_view(), name='product-search'),
]
