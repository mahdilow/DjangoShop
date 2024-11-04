from django.db import models
from django.contrib.auth.models import User
from django.core.files import File
from io import BytesIO
from PIL import Image,ImageFilter
from django_jalali.db import models as jmodels

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

    def price_display(self):
        return self.price 
    
    def get_thumbnail(self):
        if self.thumbnail:
            return self.thumbnail.url
        elif self.image:
            # Generate the thumbnail if it doesn’t exist
            self.thumbnail = self.make_thumbnail(self.image)
            # Save the model instance with the new thumbnail
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
