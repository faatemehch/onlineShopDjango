from django.contrib import admin
from .models import ProductCategory, SubCategory


# Register your models here.
class ProductCategoryAdmin( admin.ModelAdmin ):
    list_display = ['__str__', 'name']
    # list_filter = ['__str__']

    class Meta:
        model = ProductCategory


admin.site.register( ProductCategory, ProductCategoryAdmin )
admin.site.register( SubCategory )
