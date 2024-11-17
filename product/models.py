from django.db import models
from django.contrib.auth.models import User
from django.core.files import File
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from io import BytesIO
from PIL import Image,ImageFilter
from django_jalali.db import models as jmodels
from decimal import Decimal

class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    thumbnail = models.ImageField(upload_to='category_thumbnails/', blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ('name',)
    
    def __str__(self):
        return self.name

    def get_thumbnail(self):
        if self.thumbnail:
            return self.thumbnail.url
        else:
            return 'https://via.placeholder.com/240x240.jpg'

class Discount(models.Model):
    OFF_TYPE = [
        ('percentage', 'درصدی'),
        ('fixed', 'مبلغ ثابت'),
    ]
    
    title = models.CharField(max_length=100)
    off_type = models.CharField(max_length=10, choices=OFF_TYPE, default='percentage')
    amount = models.DecimalField(
        max_digits=10, 
        decimal_places=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    start_date = jmodels.jDateTimeField()
    end_date = jmodels.jDateTimeField()
    products = models.ManyToManyField('Product', blank=True, related_name='offs')
    categories = models.ManyToManyField('Category', blank=True, related_name='offs')
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} ({self.amount}{'%' if self.off_type == 'percentage' else ' تومان'})"

    def is_valid(self):
        now = timezone.now()
        return self.active and self.start_date <= now <= self.end_date

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=0)
    created_at = jmodels.jDateField(auto_now_add=True)
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='uploads/', blank=True, null=True)

    class Meta:
        ordering = ('-created_at',)
    
    def __str__(self):
        return self.name

    def get_off(self):
        now = timezone.now()
        product_off = self.offs.filter(
            active=True,
            start_date__lte=now,
            end_date__gte=now
        ).first()
        
        if product_off:
            return product_off
        
        category_off = self.category.offs.filter(
            active=True,
            start_date__lte=now,
            end_date__gte=now
        ).first()
        
        return category_off

    def get_off_price(self):
        off = self.get_off()
        if not off:
            return self.price

        if off.off_type == 'percentage':
            off_amount = (self.price * Decimal(off.amount)) / Decimal(100)
        else:
            off_amount = off.amount

        return max(self.price - off_amount, Decimal('0')) 

    def price_display(self):
        off_price = self.get_off_price()
        return off_price if off_price < self.price else self.price
    
    def get_thumbnail(self):
        if self.thumbnail:
            return self.thumbnail.url
        elif self.image:
            self.thumbnail = self.make_thumbnail(self.image)
            self.save(update_fields=['thumbnail'])
            return self.thumbnail.url
        else:
            return 'https://via.placeholder.com/240x240.jpg'
    
    def make_thumbnail(self, image, size=(500, 500)):
        img = Image.open(image)
        img = img.convert('RGB')
        
        # Progressive downscaling
        while img.size[0] > 2 * size[0] and img.size[1] > 2 * size[1]:
            img = img.resize((img.size[0] // 2, img.size[1] // 2), Image.LANCZOS)

        # Final resize to target size
        img = img.resize(size, Image.LANCZOS)
        img = img.filter(ImageFilter.SHARPEN)
        
        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=95)
        
        thumbnail = File(thumb_io, name=image.name)
        return thumbnail

    def get_rating(self):
        reviews_total = sum(review.rating for review in self.reviews.all())
        return reviews_total / self.reviews.count() if self.reviews.count() > 0 else 0

class Review(models.Model):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    rating = models.IntegerField(default=3)
    content = models.TextField()
    created_by = models.ForeignKey(User, related_name='reviews', on_delete=models.CASCADE)
    created_at = jmodels.jDateTimeField(auto_now_add=True)