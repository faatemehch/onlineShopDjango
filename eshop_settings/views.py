from django.shortcuts import render
from eshop_products_category.models import ProductCategory
from .models import Slider, SiteSetting
from eshop_products.models import Product


# Create your views here.

# home view
def home_page(request):
    sliders = Slider.objects.all()
    newest_products = Product.objects.all().order_by( '-date_added' )[:3]
    most_sell_products = Product.objects.all().order_by( '-sell_count' )[:3]
    most_visited_products = Product.objects.all().order_by( '-visit_count' )[:3]
    context = {'title': 'صفحه اصلی',
               'sliders': sliders,
               'newest_products': newest_products,
               'most_sell_products': most_sell_products,
               'most_visited_products':most_visited_products
               }

    return render( request, 'home_page.html', context )


# header code behind
def header(request):
    categories = ProductCategory.objects.all()
    context = {
        'categories': categories
    }
    return render( request, 'shared/header.html', context )


# footer code behind
def footer(request):
    context = {}
    return render( request, 'shared/footer.html', context )


# about us view
def about_page(request):
    context = {
        'site_settings': SiteSetting.objects.last()
    }
    return render( request, 'about_us_page.html', context )


# handle page not found error
def handler404(request, exception):
    context = {'title': 'فروشگاه اینترنتی|۴۰۴ ارور'}
    return render( request, '404.html', context )
