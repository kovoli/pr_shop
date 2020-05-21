from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
# for slugfield
from django.urls import reverse
from django.template.defaultfilters import slugify
from unidecode import unidecode
# Image
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit

class Category(MPTTModel):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    short_description = models.TextField(blank=True, null=True)

    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.name))
        super(Category, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('products:category', args=[self.slug])

    def __str__(self):
        return self.name

    class MPTTMeta:
        order_insertion_by = ['-name']

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        #indexes = [models.Index(fields=['slug'])]


# -------------- SHOP ---------------
class Shop(models.Model):
    name = models.CharField(max_length=100)
    image_store = ProcessedImageField(upload_to='shop_image/',
                                      blank=True,
                                      processors=[ResizeToFit(80, None)],
                                      format='JPEG',
                                      options={'quality': 100})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Магазин'
        verbose_name_plural = 'Магазины'


class Brand(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)


    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products:brand', args=[self.slug])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.name))
        super(Brand, self).save(*args, **kwargs)

    class Meta:
        ordering = ['name']
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'
        #indexes = [models.Index(fields=['slug'])]


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    oldprice = models.DecimalField(decimal_places=2, max_digits=10, blank=True, null=True)
    link = models.TextField()

    # Related objects
    category = TreeForeignKey('Category', related_name='products', on_delete=models.CASCADE)
    shop = models.ForeignKey('Shop', related_name='shop', on_delete=models.CASCADE)
    brand = models.ForeignKey('Brand', related_name='brand', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        #indexes = [models.Index(fields=['slug'])]
