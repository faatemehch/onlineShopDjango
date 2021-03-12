from django.contrib.auth.models import User
from django.db import models
import os
from django.db.models import Q
from eshop_products_category.models import ProductCategory, SubCategory


class ProductManager( models.Manager ):
    def get_active_products(self):
        return self.get_queryset().filter( active=True ).order_by( '-date_added' )

    def get_cheapest_products(self):
        return self.get_queryset().filter( active=True ).order_by( 'price' )

    def get_the_most_expensive_products(self):
        return self.get_queryset().filter( active=True ).order_by( '-price', '-date_added' )

    def get_newest_products(self):
        return self.get_queryset().filter( active=True ).order_by( '-date_added' )

    def get_product_by_id(self, product_id):
        return self.get_queryset().filter( id=product_id ).first()

    def search(self, query):
        lookup = Q( title__icontains=query ) | \
                 Q( description__icontains=query ) | \
                 Q( tag__title__icontains=query )
        return self.get_queryset().filter( lookup, active=True ).distinct()

    def get_products_by_category(self, category_name):
        lookup = Q( categories__name__iexact=category_name ) | \
                 Q( sub_categories__name__iexact=category_name )
        return self.get_queryset().filter( lookup, active=True ).order_by( '-date_added' )


def get_file_name_ext(file_path):
    base_name = os.path.basename( file_path )
    name, ext = os.path.splitext( base_name )
    return name, ext


def upload_image_path(instance, fileName):
    name, ext = get_file_name_ext( fileName )
    final_name = f'{instance.id}/{instance.title}/{ext}'
    return f'products/products_images/{final_name}'


# creat products model
class Product( models.Model ):
    title = models.CharField( max_length=150, verbose_name='نام محصول' )
    description = models.TextField( verbose_name='توضیحات محصول' )
    price = models.IntegerField( verbose_name='قیمت محصول' )
    discounted_price = models.IntegerField( verbose_name='قیمت محصول بعد از تخفیف', null=True, blank=True )
    quantity = models.IntegerField( verbose_name='تعداد در انبار' )
    active = models.BooleanField( verbose_name='موجود/ناموجود', default=False )
    date_added = models.DateTimeField( auto_now_add=True, verbose_name='تاریخ اضافه شدن محصول', blank=True, null=True )
    image = models.ImageField( null=True, blank=True, verbose_name='تصویر محصول', upload_to=upload_image_path )
    sell_count = models.IntegerField( null=True, blank=True, verbose_name='تعداد فروش محصول', default=0 )
    categories = models.ManyToManyField( ProductCategory, null=True, blank=True, verbose_name='دسته‌بندی' )
    sub_categories = models.ManyToManyField( SubCategory, null=True, blank=True, verbose_name='زیر دسته‌بندی' )
    visit_count = models.IntegerField( default=0, null=True, blank=True, verbose_name='تعداد بازدید' )

    objects = ProductManager()

    def get_price(self):
        if self.discounted_price:
            return self.discounted_price
        else:
            return self.price

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f'/products/{self.id}'

    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'


class Comment( models.Model ):
    product = models.ForeignKey( Product, on_delete=models.CASCADE, verbose_name='محصول' )
    owner = models.ForeignKey( User, on_delete=models.CASCADE, verbose_name='نام کاربری' )
    full_name = models.CharField( max_length=150, verbose_name='نام و نام‌خانوادگی' )
    email = models.EmailField( verbose_name='ایمیل' )
    comment = models.TextField( null=True, blank=True, verbose_name='نظر' )
    date_added = models.DateTimeField( auto_now_add=True, verbose_name='تاریخ اضافه شدن نظر', blank=True, null=True )

    def __str__(self):
        return self.product

    class Meta:
        verbose_name = 'نظر کاربر'
        verbose_name_plural = 'نظرات کاربران'


class Visited_Ip_product( models.Model ):
    product = models.ForeignKey( Product, verbose_name='محصول', null=True, blank=True, on_delete=models.CASCADE )
    user_ip = models.TextField( verbose_name='آدرس‌ها' )

    def __str__(self):
        return self.user_ip

    class Meta:
        verbose_name = 'آدرس ip کاربر'
        verbose_name_plural = 'آدرس ip کاربر'
