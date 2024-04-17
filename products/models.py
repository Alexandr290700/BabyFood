from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse


User = get_user_model()


class Catalog(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    

class FoodCategory(models.Model):
    name = models.CharField(max_length=150)
    image = models.ImageField(upload_to='media/food_category/', null=True, blank=True)
    catalog = models.ForeignKey(Catalog, on_delete=models.CASCADE, related_name='food_categories')

    def __str__(self):
        return f"{self.name} ({self.catalog.name})"


class Brand(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    

class Product(models.Model):
    name = models.CharField(max_length=300)
    description = models.TextField()
    price = models.DecimalField(max_digits=15, decimal_places=2)
    default_image = models.ImageField(upload_to='media/defaults/', null=True, blank=True)
    weight = models.IntegerField()
    is_arrived = models.BooleanField(default=True)
    rating = models.IntegerField(default=1, choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])
    in_stock = models.BooleanField(default=True)
    discount = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    food_category = models.ForeignKey(FoodCategory, on_delete=models.CASCADE, related_name='products')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return f"{self.name} - {self.brand.name}"
    
    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"pk": self.pk})
    
    

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_images')
    images = models.ImageField(upload_to='media/products/')

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
