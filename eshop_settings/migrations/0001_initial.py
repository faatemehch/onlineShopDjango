# Generated by Django 3.1.5 on 2021-01-20 06:12

from django.db import migrations, models
import eshop_settings.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Slider',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='عنوان')),
                ('link', models.URLField(blank=True, null=True, verbose_name='آدرس')),
                ('image', models.ImageField(blank=True, null=True, upload_to=eshop_settings.models.upload_image_path, verbose_name='تصویر')),
            ],
            options={
                'verbose_name': 'اسلایدر',
                'verbose_name_plural': 'اسلایدر\u200cها',
            },
        ),
    ]