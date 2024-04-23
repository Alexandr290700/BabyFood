from typing import Any
from django.contrib import admin
from django import forms
from .models import (Catalog,
                     FoodCategory,
                     Brand,
                     Product,
                     CarouselItem,
                     ReviewProduct,
                     Favorite,
                     Cart,
                     Order,
                     Promotion,
                     ExtraInfo,
                     ProductImage,
                     ProductBrandImage,
                     BrandImage,
                     Review
                     )

admin.site.register([Catalog, FoodCategory, Brand, CarouselItem, ReviewProduct, Favorite, Cart, Order, Promotion,ExtraInfo, ProductImage, ProductBrandImage, BrandImage, Review])

class ProductAdminForm(forms.ModelForm):
    extra_info = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'cols': 80, 'rows': 10})
        }


class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm

    def save_model(self, request, obj, form, change):
        extra_info = form.cleaned_data.get('extra_info')
        if extra_info:
            obj.extra_info = extra_info.split(',')
        super().save_model(request, obj, form, change)

admin.site.register(Product, ProductAdmin)
