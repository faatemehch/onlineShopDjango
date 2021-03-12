from django.contrib import admin
from .models import (
    Order,
    OrderDetail,
    Coupon,
    Province,
    City
)


class OrderAdmin( admin.ModelAdmin ):
    list_display = ['__str__', 'is_paid', 'is_send', 'payment_date']


class CityAdmin( admin.ModelAdmin ):
    list_display = ['__str__', 'province']


# Register your models here.

admin.site.register( Order, OrderAdmin )
admin.site.register( OrderDetail )
admin.site.register( Coupon )
admin.site.register( Province )
admin.site.register( City, CityAdmin )
