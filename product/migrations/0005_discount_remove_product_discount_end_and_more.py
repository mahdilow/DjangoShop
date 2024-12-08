# Generated by Django 4.2.16 on 2024-11-17 13:52

import django.core.validators
from django.db import migrations, models
import django_jalali.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_offer_product_discount_end_product_discount_price_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('off_type', models.CharField(choices=[('percentage', 'درصدی'), ('fixed', 'مبلغ ثابت')], default='percentage', max_length=10)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=5, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('start_date', django_jalali.db.models.jDateTimeField()),
                ('end_date', django_jalali.db.models.jDateTimeField()),
                ('active', models.BooleanField(default=True)),
                ('categories', models.ManyToManyField(blank=True, related_name='offs', to='product.category')),
            ],
        ),
        migrations.RemoveField(
            model_name='product',
            name='discount_end',
        ),
        migrations.RemoveField(
            model_name='product',
            name='discount_price',
        ),
        migrations.RemoveField(
            model_name='product',
            name='discount_start',
        ),
        migrations.RemoveField(
            model_name='product',
            name='offer',
        ),
        migrations.DeleteModel(
            name='Offer',
        ),
        migrations.AddField(
            model_name='discount',
            name='products',
            field=models.ManyToManyField(blank=True, related_name='offs', to='product.product'),
        ),
    ]
