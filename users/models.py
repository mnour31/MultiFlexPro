from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django_countries.fields import CountryField
# Create your models here.





class Profile(models.Model):
    MONTH_CHOICES = [
        ('ذكر' , 'ذكر'),
        ('انثي' ,'انثى')
    ]

    user = models.OneToOneField(User , on_delete=models.CASCADE)
    id = models.AutoField(primary_key=True)
    country = CountryField()
    bio = models.TextField(default='لا يوجد وصف')
    full_name = models.CharField(max_length=150 , default=' ')
    profile_img = models.ImageField(upload_to='profile_img/%y/%m/%d' , default='user_img.jpg')
    age = models.IntegerField( null=True, blank=True)
    job_title = models.CharField(max_length=150 , default='no job')
    created_at = models.DateTimeField(auto_now_add=True)
    type_per =  models.CharField(max_length=9, choices=MONTH_CHOICES, default='did not choose')
    slug = models.SlugField(unique=True ,null=True, blank=True , allow_unicode=True)

    def __str__(self):
        return self.user.username

    def save(self , *args, **kwargs):
        self.slug = slugify(self.user.username)
        try:
            self.full_name = f'{self.user.first_name} {self.user.last_name}'
        except:
            pass

        super(Profile , self).save(*args, **kwargs)
