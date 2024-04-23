from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CatalogViewSet,
    FoodCategoryViewSet,
    BrandViewSet,
    ProductViewSet,
    CarouselItemViewSet,
    ReviewViewSet,
    FavoriteListAPIView,
    CartViewSet,
    OrderViewSet,
    ProductSearchAPIView,
    PromotionViewSet,
    BrandImageViewSet,
    NewProductViewSet,
    PopularProductViewSet,
    RecommendedProductViewSet,
)


router = DefaultRouter()

router.register('catalogs', CatalogViewSet)
router.register('food_categories', FoodCategoryViewSet)
router.register('brands', BrandViewSet)
router.register('products', ProductViewSet)
router.register('carousel_items', CarouselItemViewSet)
router.register('reviews', ReviewViewSet)
router.register(r'carts', CartViewSet)
router.register(r'orders', OrderViewSet)
router.register('promotion', PromotionViewSet)
router.register('brand_image', BrandImageViewSet)
router.register(r'new-products', NewProductViewSet, basename='new-products')
router.register(r'popular-products', PopularProductViewSet, basename='popular-products')
router.register(r'recommended-products', RecommendedProductViewSet, basename='recommended-products')

urlpatterns = [
    path('', include(router.urls)),
    path('users/favorites/', FavoriteListAPIView.as_view()),
    path('search/', ProductSearchAPIView.as_view(), name='product-search'),
]
