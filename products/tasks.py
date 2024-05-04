from celery import shared_task
from django.utils import timezone
from .models import Product


@shared_task
def upate_new_product_status():
    new_products = Product.objects.filter(arrived=True)

    for product in new_products:
        if timezone.now() - product.created_at >= timezone.timedelta(days=14):
            product.arrived = False
            product.save()
