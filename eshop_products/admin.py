from django.contrib import admin
from .models import Product, Comment, Visited_Ip_product


# Register your models here.
class ProductAdmin( admin.ModelAdmin ):
    list_display = ['__str__', 'active', 'quantity']
    list_filter = ['quantity', 'active', 'date_added']

    class Meta:
        model = Product


class CommentAdmin( admin.ModelAdmin ):
    list_display = ['__str__', 'owner', 'date_added']

    class Meta:
        model = Product


class VisitedCountAdmin( admin.ModelAdmin ):
    list_display = ['__str__', 'product']


admin.site.register( Product, ProductAdmin )
admin.site.register( Comment, CommentAdmin )
admin.site.register( Visited_Ip_product, VisitedCountAdmin )
