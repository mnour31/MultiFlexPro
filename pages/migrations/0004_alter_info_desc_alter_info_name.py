# Generated by Django 4.1.5 on 2023-02-05 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0003_delete_customization_delete_store'),
    ]

    operations = [
        migrations.AlterField(
            model_name='info',
            name='desc',
            field=models.TextField(verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='info',
            name='name',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Name'),
        ),
    ]