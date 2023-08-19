from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.utils import timezone
from hitcount.models import HitCountMixin, HitCount
from ckeditor.fields import RichTextField
from django.contrib.contenttypes.fields import GenericRelation

# Create your models here.
def arabic_slugify(str):
    str = str.replace(" ", "-")
    str = str.replace(",", "-")
    str = str.replace("(", "-")
    str = str.replace(")", "")
    str = str.replace("؟", "")
    return str


class Customer(models.Model):
    user = models.OneToOneField(User , null=True , blank=True , on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200)
    def __str__(self):
        return self.name

class Shop(models.Model):
    LANGUAGES = [
    ('arabic','عربي'),
    ('english','english'),
    ]

    TEMPLATES = [
        ('nour','nour'),
        ('food','food'),
    ]
    CURRENCYS = [
        ('EGP','EGP'),
        ('USD','USD'),
    ] 

    name = models.CharField(max_length=100, blank=True, null=True)
    logo = models.ImageField(upload_to='shop/logos/%y/%m/%d' , default='logo.png')
    user = models.OneToOneField(User , on_delete=models.CASCADE , blank=True, null=True)
    bio = models.TextField(default='لا يوجد وصف')
    currency = models.CharField(max_length=30, choices=CURRENCYS)
    slug = models.SlugField(unique=True ,null=True, blank=True , allow_unicode=True)
    lang = models.CharField(max_length=30, choices=LANGUAGES)
    template = models.CharField(max_length=30, choices=TEMPLATES)
    is_slider = models.BooleanField(default=True)
    is_brands = models.BooleanField(default=True)
    # social media links
    facebook = models.URLField(max_length=200 , null=True, blank=True)
    instagram = models.URLField(max_length=200 , null=True, blank=True)
    twitter = models.URLField(max_length=200 , null=True, blank=True)
    linkedin = models.URLField(max_length=200 , null=True, blank=True)
    pinterest = models.URLField(max_length=200 , null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self  ,*args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            if not self.slug:
                self.slug = arabic_slugify(self.name)
        super(Shop , self).save(*args, **kwargs)

class Product(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    desc = models.TextField(max_length=150 , blank=True, null=True)
    content = RichTextField(default='المحتوي')
    categorie = models.ForeignKey('Categorie' ,  on_delete=models.SET_NULL , blank=True, null=True)
    shop = models.ForeignKey(Shop , on_delete=models.CASCADE , blank=True, null=True)
    price =  models.FloatField(default=0)
    discount =  models.FloatField(default=0)
    digital = models.BooleanField(default=False , blank=True, null=True)
    image = models.ImageField(upload_to='product_images/%y/%m/%d' , default='shop.webp')
    slug = models.SlugField(null=True, blank=True )
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    hit_count_generic = GenericRelation(
        HitCount, object_id_field='object_pk',
        related_query_name='hit_count_generic_relation')

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
    def get_discount(self):
        discount = 0
        discount = self.price - self.discount
        return discount
    def get_rating(self):
        reviews = self.reviews.all()
        total_ratings = sum(review.rating for review in reviews)
        if reviews.count()>0:
            return total_ratings / reviews.count()
        else:
            return 0

    def save(self , *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            if not self.slug:
                self.slug = arabic_slugify(self.title)
        super(Product , self).save(*args, **kwargs)

class Order(models.Model):
    customer = models.ForeignKey(Customer , on_delete=models.SET_NULL ,null=True , blank=True )
    shop = models.ForeignKey(Shop , on_delete=models.SET_NULL ,null=True , blank=True )
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100 , null=True)
    # orders status after complete
    shipping = models.BooleanField(default=False)
    delivery = models.BooleanField(default=False)
    throwback = models.BooleanField(default=False)
    def __str__(self):
        return str(self.id)

class OrderItem(models.Model):
    product = models.ForeignKey(Product , null=True , blank=True , on_delete=models.SET_NULL)
    order = models.ForeignKey(Order , null=True , blank=True , on_delete=models.SET_NULL)
    quantity = models.IntegerField(default=0 , null=True , blank=True)
    date_added =  models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer , on_delete=models.SET_NULL ,null=True , blank=True )
    order = models.ForeignKey(Order , on_delete=models.SET_NULL ,null=True , blank=True , related_name='shipping_address')
    address = models.CharField(max_length=200, blank=True, null=False)
    city = models.CharField(max_length=200, blank=True, null=False)
    state = models.CharField(max_length=200, blank=True, null=False)
    zipcode = models.CharField(max_length=200, blank=True, null=False)
    date_added =  models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.address

class Review(models.Model):
    STARS = [
        (20 ,20),
        (40 ,40),
        (60 ,60),
        (80 ,80),
        (100 ,100),
    ]
    product = models.ForeignKey(Product , related_name='reviews' , on_delete=models.CASCADE)
    rating = models.IntegerField(default=60 , choices=STARS)
    content = models.TextField()
    created_by = models.ForeignKey(Customer ,on_delete=models.CASCADE , related_name='customer' )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.title

class Page(models.Model):
    title = models.CharField(max_length=100)
    content = RichTextField(default='المحتوي')
    slug = models.SlugField(null=True, blank=True )
    shop = models.ForeignKey(Shop , related_name='pages', on_delete=models.CASCADE , blank=True, null=True)

    def __str__(self):
        return self.title
    def save(self , *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            if not self.slug:
                self.slug = arabic_slugify(self.title)
        super(Page , self).save(*args, **kwargs)

class Categorie(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    father = models.ForeignKey('self' , limit_choices_to= {'is_father':True} ,on_delete=models.CASCADE , blank=True, null=True )
    is_father = models.BooleanField(default=False)
    shop = models.ForeignKey(Shop , related_name='categories' , on_delete=models.CASCADE , blank=True, null=True)
    img = models.ImageField(upload_to='categories' , default='categorise.webp')



    def __str__(self):
        return str(self.name)

