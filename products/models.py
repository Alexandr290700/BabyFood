from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from ckeditor.fields import RichTextField
from tinymce.models import HTMLField


User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=150)
    image = models.ImageField(upload_to='media/food_category/', null=True, blank=True)

    def __str__(self):
        return f"{self.name}"
    

class SubCategory(models.Model):
    title = models.CharField(max_length=150)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title}"


class Brand(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='media/brand/')

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=300)
    description = HTMLField()
    arrived = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=15, decimal_places=2)
    default_image = models.ImageField(upload_to='media/defaults/', null=True, blank=True)
    weight = models.IntegerField()
    rating = models.IntegerField(default=1, choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])
    discount = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='products', blank=True, null=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='products')
    extra_info = models.TextField(default='[]')

    def __str__(self):
        return f"{self.name} - {self.brand.name}"
    
    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"pk": self.pk})   
    

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_images')
    image = models.ImageField(upload_to='media/products/')

    def __str__(self):
        return self.product.name


class CarouselItem(models.Model):
    images = models.ImageField(upload_to='media/carousel/')
    description = models.TextField()

    def __str__(self):
        return f"Carousel Item {self.id}"
    

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    rating = models.IntegerField(default=1, choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.name} for {self.product.name}"
    

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='favorites')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Favorite by {self.user.name} - {self.product.name}"


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carts')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='carts')
    created_at = models.DateTimeField(auto_now_add=True)
    count = models.IntegerField(default=1)

    def __str__(self):
        return f"Cart of {self.user.name} - {self.product.name}"
    

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    product = models.ManyToManyField(Product, through='OrderItem')
    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=150)
    email = models.EmailField()
    total_price = models.DecimalField(max_digits=15, decimal_places=2)
    shipping_address = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Order {self.id} by {self.user.name} - Address: {self.shipping_address}'
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
    price = models.DecimalField(max_digits=15, decimal_places=2)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f'Order Item: {self.product.name} - {self.quantity}'
    

class Promotion(models.Model):
    image = models.ImageField(upload_to='media/promotion_image/')
    link = models.URLField(blank=True)

    def __str__(self):
        return f'Promotion {self.pk}'

class CustomerReview(models.Model):
    text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=150, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.text} - {self.user} - {self.created_at}'
