# Generated by Django 4.1.5 on 2023-02-06 08:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0013_remove_categories_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categories',
            name='blog',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='blog.blog'),
        ),
    ]