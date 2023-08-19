from django.db import models
from shop.models import Shop

# Create your models here.



class Brand(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to='shops/brand/%y/%m/%d' , default='brand.jpg')
    shop = models.ForeignKey(Shop, null=True , blank=True , on_delete=models.CASCADE , related_name='brands')

    def __str__(self):
        return  self.name

class Slider(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    url = models.URLField(default='#')
    image = models.ImageField(upload_to='shops/slider/%y/%m/%d' , default='brand.jpg')
    shop = models.ForeignKey(Shop, null=True , blank=True , on_delete=models.CASCADE , related_name='slider')

    def __str__(self):
        return  self.name