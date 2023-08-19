from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.utils import timezone
from hitcount.models import HitCountMixin, HitCount
from ckeditor.fields import RichTextField
# Create your models here.
# Create your models here.
def arabic_slugify(str):
    str = str.replace(" ", "-")
    str = str.replace(",", "-")
    str = str.replace("(", "-")
    str = str.replace(")", "")
    str = str.replace("؟", "")
    return str

class Cv(models.Model):
    Freelance = [
        ('Available','Available'),
        ('Unavailable','Unavailable'),
    ]
    name = models.CharField(max_length=100,blank=True, null=True)
    image = models.ImageField(upload_to='cv/user-cv/%y/%m/%d' , default='shop.webp')
    user = models.OneToOneField(User , on_delete=models.CASCADE , blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    slug = models.SlugField(unique=True ,null=True, blank=True , allow_unicode=True)
    job_title = models.CharField(max_length=100,blank=True, null=True)
    about = models.TextField(max_length=300 ,blank=True, null=True)
    degree = models.CharField(max_length=100,blank=True, null=True)
    phone = models.IntegerField( blank=True, null=True )
    address = models.CharField(max_length=100,blank=True, null=True)
    birthday = models.CharField(max_length=100,blank=True, null=True)
    experience = models.IntegerField(blank=True, null=True , default=2)
    email = models.EmailField()
    freelance = models.CharField(max_length=30,blank=True, null=True , choices=Freelance)
    p_Complete = models.IntegerField(blank=True, null=True , default=2)
    happy_clients = models.IntegerField(blank=True, null=True , default=100)
    # social media links
    facebook = models.URLField(max_length=200 , null=True, blank=True)
    instagram = models.URLField(max_length=200 , null=True, blank=True)
    twitter = models.URLField(max_length=200 , null=True, blank=True)
    linkedin = models.URLField(max_length=200 , null=True, blank=True)
    pinterest = models.URLField(max_length=200 , null=True, blank=True)
    github = models.URLField(max_length=200 , null=True, blank=True)

    def __str__(self):
        return self.name
    def save(self  ,*args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            if not self.slug:
                self.slug = arabic_slugify(self.name)
        super(Cv , self).save(*args, **kwargs)

class JobTitle(models.Model):
    cv = models.ForeignKey(Cv , on_delete=models.CASCADE , related_name='jobtitles' , null=True , blank=True)
    name = models.CharField(max_length=100, blank=True, null=True)

class Skille(models.Model):
    PROGRISE = [
        (10,10),
        (20,20),
        (30,30),
        (40,40),
        (50,50),
        (60,60),
        (70,70),
        (80,80),
        (90,90),
        (100,100),

    ]
    cv = models.ForeignKey(Cv , on_delete=models.CASCADE , related_name='skilles' , null=True , blank=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    progrise = models.IntegerField(choices=PROGRISE , default=30)

    def __str__(self):
        return self.name

class Experience(models.Model):
    cv = models.ForeignKey(Cv , on_delete=models.CASCADE , related_name='experiences' , null=True , blank=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    company_name = models.CharField(max_length=100, blank=True, null=True)
    date_from =  models.DateTimeField(blank=True, null=True)
    date_to =  models.DateTimeField(blank=True, null=True)
    desc = models.TextField(max_length=200)
    def __str__(self):
        return self.name

class Service(models.Model):
    cv = models.ForeignKey(Cv , on_delete=models.CASCADE , related_name='services' , null=True , blank=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    image = models.ImageField(upload_to='cv/service/%y/%m/%d' , default='shop.webp')
    desc = models.TextField(max_length=100)

    def __str__(self):
        return self.name

class Portfolio(models.Model):
    cv = models.ForeignKey(Cv , on_delete=models.CASCADE , related_name='portfolios' , null=True , blank=True)
    image = models.ImageField(upload_to='cv/portfolios/%y/%m/%d' , default='shop.webp')
    name = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return 

class Testimonial(models.Model):
    cv = models.ForeignKey(Cv , on_delete=models.CASCADE , related_name='testimonials' , null=True , blank=True)
    client_name = models.CharField(max_length=50, blank=True, null=True)
    what_he_say =  models.TextField(max_length=200 , blank=True, null=True)
    image = models.ImageField(upload_to='cv/testimonials/%y/%m/%d' , default='shop.webp')
    def __str__(self):
        return self.cv.name
