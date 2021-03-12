from django.db import models
import os


def get_file_name_ext(file_path):
    base_name = os.path.basename( file_path )
    name, ext = os.path.splitext( base_name )
    return name, ext


def upload_image_path(instance, fileName):
    name, ext = get_file_name_ext( fileName )
    final_name = f'{instance.id}/{instance.title}/{ext}'
    return f'products/slider_image/{final_name}'


class Slider( models.Model ):
    title = models.CharField( max_length=150, verbose_name='عنوان' )
    link = models.URLField( max_length=200, verbose_name='آدرس', null=True, blank=True )
    image = models.ImageField( upload_to=upload_image_path, null=True, blank=True, verbose_name='تصویر' )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'اسلایدر'
        verbose_name_plural = 'اسلایدر‌ها'


class SiteSetting( models.Model ):
    title = models.CharField( max_length=150, verbose_name='عنوان' )
    address = models.CharField( max_length=400, verbose_name='آدرس' )
    phone = models.CharField( max_length=50, verbose_name='تلفن' )
    fax = models.CharField( max_length=50, verbose_name='فکس' )
    email = models.EmailField( max_length=100, verbose_name='ایمیل' )
    about_us_text = models.TextField( verbose_name='درباره ما' )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'تنظیمات سایت'
        verbose_name_plural = 'مدیریت تنظیمات'
