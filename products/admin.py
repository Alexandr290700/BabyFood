from django.contrib import admin

from .models import Catalog, FoodCategory, Brand, Product, ProductImage, CarouselItem, Review, Favorite, Cart, Order, Promotion


admin.site.register([Catalog, FoodCategory, Brand, Product, ProductImage, CarouselItem, Review, Favorite, Cart, Order, Promotion])
