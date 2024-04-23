# Generated by Django 4.2 on 2024-04-23 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_product_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='status',
            field=models.CharField(choices=[('New', 'New'), ('Regular', 'Regular')], default='Regular', max_length=20),
        ),
    ]
