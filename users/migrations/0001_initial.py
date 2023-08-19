# Generated by Django 4.1.5 on 2023-01-14 19:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('country', django_countries.fields.CountryField(max_length=2)),
                ('img', models.ImageField(default='user_img.jpg', upload_to='profile_img/%y/%m/%d')),
                ('age', models.IntegerField(blank=True, null=True)),
                ('job_title', models.CharField(default='no job', max_length=150)),
                ('type_per', models.CharField(choices=[('ذكر', 'ذكر'), ('انثي', 'انثى')], default='did not choose', max_length=9)),
                ('slug', models.SlugField(allow_unicode=True, blank=True, null=True, unique=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]