from django.db import models


# Create your models here.

class ProductCategory( models.Model ):
    title = models.CharField( max_length=150, verbose_name='عنوان' )
    name = models.CharField( max_length=150, verbose_name='عنوان در URL' )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'ماژول دسته‌بندی محصولات'


class SubCategory( models.Model ):
    title = models.CharField( verbose_name='عنوان', max_length=150 )
    name = models.CharField( max_length=150, verbose_name='عنوان در url' )
    category = models.ForeignKey( ProductCategory, related_name='category', verbose_name='دسته‌ اصلی', blank=True,
                                  null=True, on_delete=models.CASCADE )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'زیردسته‌بندی'
        verbose_name_plural = 'زیردسته‌بندی‌‌ها'
