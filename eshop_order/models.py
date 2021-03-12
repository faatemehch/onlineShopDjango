from django.contrib.auth.models import User
from django.db import models
from django_jalali.db import models as jmodels
# Create your models here.
from eshop_products.models import Product


# user orders
class Order( models.Model ):
    owner = models.ForeignKey( User, on_delete=models.CASCADE, verbose_name='نام کاربری خریدار' )
    is_paid = models.BooleanField( default=False, verbose_name='پرداخت شده/پرداخت نشده' )
    payment_date = jmodels.jDateTimeField( null=True, blank=True, verbose_name='تاریخ پرداخت' )
    tracking_code = models.CharField( null=True, blank=True, verbose_name='کد رهگیری سفارش', max_length=50 )
    coupon_code = models.ForeignKey( 'Coupon', null=True, blank=True, on_delete=models.DO_NOTHING,
                                     verbose_name='کد تخفیف' )
    use_code = models.BooleanField( default=False, verbose_name='استفاده/عدم استفاده از کد تخفیف', null=True,
                                    blank=True )
    is_send = models.BooleanField( default=False, verbose_name='ارسال شده/نشده', null=True, blank=True )
    # complete order
    name = models.CharField( verbose_name='نام', max_length=50, null=True, blank=True )
    family = models.CharField( verbose_name=' نام‌خانوادگی', max_length=50, null=True, blank=True )
    post_code = models.IntegerField( verbose_name='کد پستی', null=True, blank=True )
    phone_number = models.IntegerField( verbose_name='شماره همراه', null=True, blank=True )
    province = models.ForeignKey( 'Province', verbose_name='استان', on_delete=models.CASCADE, null=True, blank=True )
    city = models.ForeignKey( 'City', verbose_name='شهر', on_delete=models.CASCADE, null=True, blank=True )
    address = models.TextField( verbose_name='آدرس', null=True, blank=True )
    description = models.TextField( verbose_name='توضیحات', null=True, blank=True )

    class Meta:
        verbose_name = 'سبد خرید'
        verbose_name_plural = 'سبد خرید کاربران'

    def __str__(self):
        return self.owner.get_username()

    def get_total_price(self):  # total price for a special order
        amount = 0
        for detail in self.orderdetail_set.all():
            if detail.product.discounted_price:
                amount += detail.product.discounted_price * detail.count
            else:
                amount += detail.price * detail.count
        if self.coupon_code is not None:
            amount -= (amount * self.coupon_code.amount) / 100
        return amount


# user detail orders
class OrderDetail( models.Model ):
    order = models.ForeignKey( Order, on_delete=models.CASCADE, verbose_name='سبد خرید' )
    product = models.ForeignKey( Product, on_delete=models.CASCADE, verbose_name='محصول' )
    price = models.IntegerField( verbose_name='قیمت محصول' )
    count = models.IntegerField( verbose_name='تعداد' )

    class Meta:
        verbose_name = 'جزئیات سبد خرید'
        verbose_name_plural = 'اطلاعات جزئیات سبد خرید'

    def __str__(self):
        return self.product.title


class Coupon( models.Model ):
    code = models.CharField( max_length=10, verbose_name='کد تخفیف' )
    amount = models.IntegerField( verbose_name='میزان تخفیف' )

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = 'کد تخفیف'
        verbose_name_plural = 'کد‌های تخفیف'


class Province( models.Model ):
    province_name = models.CharField( max_length=30, verbose_name='استان' )

    def __str__(self):
        return self.province_name

    class Meta:
        verbose_name = 'استان'
        verbose_name_plural = 'استان‌ها'


class City( models.Model ):
    province = models.ForeignKey( Province, on_delete=models.CASCADE, verbose_name='استان' )
    city_name = models.CharField( max_length=30, verbose_name='شهر' )

    def __str__(self):
        return self.city_name

    class Meta:
        verbose_name = 'شهر'
        verbose_name_plural = 'شهرها'
