from django.db import models

# Create your models here.


class ProductCategory(models.Model):
    name = models.CharField(max_length=64, unique=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(db_index=True, verbose_name='активна', default=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    image = models.ImageField(upload_to='products_images', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    quantity = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(db_index=True, verbose_name='активна', default=True)

    def __str__(self):
        return f"{self.name} | {self.category.name}"

    @staticmethod
    def get_items():
        return Product.objects.filter(is_active=True).order_by('category', 'name')
