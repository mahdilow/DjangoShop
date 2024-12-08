# Generated by Django 4.2.16 on 2024-11-17 13:11

from django.db import migrations, models
import django.db.models.deletion
import django_jalali.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_alter_product_created_at_alter_review_created_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('discount_percentage', models.PositiveIntegerField()),
                ('start_date', django_jalali.db.models.jDateTimeField()),
                ('end_date', django_jalali.db.models.jDateTimeField()),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='discount_end',
            field=django_jalali.db.models.jDateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='discount_price',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='discount_start',
            field=django_jalali.db.models.jDateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='offer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', to='product.offer'),
        ),
    ]
