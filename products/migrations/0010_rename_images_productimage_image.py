# Generated by Django 4.2 on 2024-04-23 11:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_rename_food_category_product_category'),
    ]

    operations = [
        migrations.RenameField(
            model_name='productimage',
            old_name='images',
            new_name='image',
        ),
    ]
