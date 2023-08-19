from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from datetime import *
from django.utils import timezone
from hitcount.models import HitCountMixin, HitCount
from django.contrib.contenttypes.fields import GenericRelation
from django.db.models import Q
# Create your models here.

def arabic_slugify(str):
    str = str.replace(" ", "-")
    str = str.replace(",", "-")
    str = str.replace("(", "-")
    str = str.replace(")", "")
    str = str.replace("؟", "")
    return str




class Blog(models.Model):
    LANGUAGES = [
        ('arabic','عربي'),
        ('english','english'),
    ]

    TEMPLATES = [
        ('nour','nour'),
    ]

    name = models.CharField(max_length=50, blank=True, null=True , unique=True)
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    logo = models.ImageField(upload_to='blog/logos/%y/%m/%d' , default='logo.png')
    email = models.EmailField(null=True , unique=True)
    bio = models.TextField(default='bio not found')
    slug = models.SlugField(unique=True ,null=True, blank=True , allow_unicode=True)
    lang = models.CharField(max_length=30, choices=LANGUAGES)
    template = models.CharField(max_length=30, choices=TEMPLATES)
    # social media links
    facebook = models.URLField(max_length=200 , null=True, blank=True)
    instagram = models.URLField(max_length=200 , null=True, blank=True)
    twitter = models.URLField(max_length=200 , null=True, blank=True)
    linkedin = models.URLField(max_length=200 , null=True, blank=True)
    pinterest = models.URLField(max_length=200 , null=True, blank=True)

    def __str__(self ):
        return self.name

    def save(self  ,*args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            if not self.slug:
                self.slug = arabic_slugify(self.name)
        super(Blog , self).save(*args, **kwargs)

class Categories(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    father = models.ForeignKey('self' , limit_choices_to= {'is_father':True} ,on_delete=models.CASCADE , blank=True, null=True )
    is_father = models.BooleanField(default=False)
    blog = models.ForeignKey(Blog , related_name='categories', on_delete=models.CASCADE , blank=True, null=True)
    img = models.ImageField(upload_to='categories' , default='categorise.webp')



    def __str__(self):
        return str(self.name)



class Post(models.Model , HitCountMixin):
    title = models.CharField(max_length=50, blank=True, null=True)
    desc = models.TextField(max_length=150 , blank=True, null=True)
    content = RichTextField(default='المحتوي')
    blog = models.ForeignKey(Blog , on_delete=models.CASCADE , blank=True, null=True)
    categorie = models.ForeignKey(Categories ,  on_delete=models.SET_NULL , blank=True, null=True)
    image = models.ImageField(upload_to='posts/%y/%m/%d' , default='categorise.png')
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

    def save(self , *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            if not self.slug:
                self.slug = arabic_slugify(self.title)
        super(Post , self).save(*args, **kwargs)