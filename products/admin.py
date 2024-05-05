from django.contrib import admin
from django.forms import ModelForm
from tinymce.widgets import TinyMCE
from .models import Category, Brand, Product, ProductImage, CarouselItem, Review, Favorite, Cart, Order, Promotion, CustomerReview, SubCategory, MobileCarouselItem
from .utils import ArrayEditorWidget


admin.site.register([Category, Brand, ProductImage, CarouselItem, Review, Favorite, Cart, Order, Promotion, SubCategory, CustomerReview, MobileCarouselItem])



class ProductAdminForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'extra_info': ArrayEditorWidget(),
        }

class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    
    def save_model(self, request, obj, form, change):
        extra_info_json = form.cleaned_data.get('extra_info')
        if extra_info_json:
            obj.characteristics = str(extra_info_json)
        super().save_model(request, obj, form, change)


admin.site.register(Product, ProductAdmin)