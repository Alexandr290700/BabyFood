from django.contrib import admin
from django.forms import ModelForm

from .models import Catalog, FoodCategory, Brand, Product, ProductImage, CarouselItem, Review, Favorite, Cart


admin.site.register([Catalog, FoodCategory, Brand, Product, ProductImage, CarouselItem, Review, Favorite, Cart])
