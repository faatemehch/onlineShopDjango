import itertools

from django.contrib import messages
from django.core.paginator import Paginator
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import ListView
from eshop_products_category.models import ProductCategory, SubCategory
from .models import Product, Comment, Visited_Ip_product
from .forms import CommentForm
from eshop_tags.models import Tag
from eshop_order.forms import UserNewOrderForm


# ------------------- List Views ----------------------
# return all products
class ProductList( ListView ):
    template_name = 'products/products_list.html'
    paginate_by = 8

    def get_queryset(self):
        return Product.objects.all().order_by( '-date_added' )

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data( **kwargs )
        context['title'] = 'فروشگاه اینترنتی|مشاهده محصولات'
        context['inner_title'] = 'محصولات'
        return context


# return products based on price decreasingly
class CheapestProducts( ListView ):
    template_name = 'products/products_list.html'
    paginate_by = 8

    def get_queryset(self):
        return Product.objects.get_cheapest_products()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data( **kwargs )
        context['title'] = 'فروشگاه اینترنتی|مشاهده محصولات'
        context['inner_title'] = 'مشاهده محصولات براساس ارزان ترین قیمت'
        return context


# return products based on price increasingly
class ExpensiveProducts( ListView ):
    template_name = 'products/products_list.html'
    paginate_by = 8

    def get_queryset(self):
        return Product.objects.get_the_most_expensive_products()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data( **kwargs )
        context['title'] = 'فروشگاه اینترنتی|مشاهده محصولات'
        context['inner_title'] = 'مشاهده محصولات براساس گران ترین قیمت'
        return context


# return active products
class ActiveProducts( ListView ):
    template_name = 'products/products_list.html'
    paginate_by = 8

    def get_queryset(self):
        return Product.objects.get_active_products()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data( **kwargs )
        context['title'] = 'فروشگاه اینترنتی|مشاهده محصولات'
        context['inner_title'] = 'مشاهده کالاهای موجود'
        return context


# return products based on date added(newest)
class NewestProducts( ListView ):
    template_name = 'products/products_list.html'
    paginate_by = 8

    def get_queryset(self):
        return Product.objects.get_newest_products()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data( **kwargs )
        context['title'] = 'فروشگاه اینترنتی|مشاهده محصولات'
        context['inner_title'] = 'مشاهده جدیدترین محصولات'
        return context


# search products
class SearchProductView( ListView ):
    template_name = 'products/products_list.html'
    paginate_by = 8

    def get_queryset(self):
        request = self.request
        query = request.GET.get( 'q' )  # get the value in search box
        if query is not None:
            return Product.objects.search( query )  # return search result
        return not Product.objects.none()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data( **kwargs )
        if len( Product.objects.search( self.request.GET.get( 'q' ) ) ) == 0:
            context['inner_title'] = 'محصولی با نام مورد نظر یافت نشد'
        else:
            context['inner_title'] = 'مشاهده محصولات براساس جستجو'
        context['title'] = 'فروشگاه اینترنتی|مشاهده نتیجه جستجو'
        return context


# categories
class ProductListByCategory( ListView ):
    template_name = 'products/products_list.html'
    paginate_by = 8

    def get_queryset(self):
        category_name = self.kwargs['category_name']
        category = ProductCategory.objects.filter( name__iexact=category_name ).first() or SubCategory.objects.filter(
            name__iexact=category_name ).first()
        # if there exist category or sub_category return it's products
        if category is None:
            raise Http404( 'صفحه مورد نظر یافت نشد!' )
        return Product.objects.get_products_by_category( category_name )

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data( **kwargs )
        category_name = self.kwargs['category_name']
        context['inner_title'] = 'مشاهده محصولات براساس دسته‌بندی'
        context['title'] = f'فروشگاه اینترنتی|مشاهده دسته‌بندی {category_name}'
        return context


def product_categories_partial(request):
    categories = ProductCategory.objects.all()
    sub_categories = SubCategory.objects.all()
    context = {
        'categories': categories,
        'sub_categories': sub_categories
    }
    return render( request, 'products/product_category_partial.html', context )


# ------------------- Detail view ---------------------
# grouping items
def my_grouper(n, iterable):
    args = [iter( iterable )] * n
    return ([e for e in t if e is not None] for t in itertools.zip_longest( *args ))


def product_detail(request, *args, **kwargs):
    product_id = kwargs['productId']  # get considered id
    comment_form = CommentForm( request.POST or None )  # comment form
    product = Product.objects.get_product_by_id( product_id )
    related_products = Product.objects.get_queryset().filter( categories__product=product ).distinct()
    new_order_form = UserNewOrderForm( request.POST or None, initial={'product_id': product_id} )  # order form
    grouped_related_products = my_grouper( 4, related_products )
    tag = Tag.objects.filter( product=product )
    grouped_related_products = list( zip( grouped_related_products ) )
    grouped_related_products = [i for i in grouped_related_products[0][0] if i != product]
    if product is None:  # if product is not find
        raise Http404( 'محصول مورد نظر یافت نشد' )
    if comment_form.is_valid() and request.method == 'POST':
        if not request.user.is_authenticated:
            messages.warning( request, 'ابتدا باید وارد سایت شوید!' )
            return redirect( 'login' )
        full_name = comment_form.cleaned_data.get( 'full_name' )
        email = comment_form.cleaned_data.get( 'email' )
        comment = comment_form.cleaned_data.get( 'comment' )
        Comment.objects.create( owner=request.user, product_id=product_id, full_name=full_name, email=email,
                                comment=comment )
        messages.success( request, 'نظر شما با موفقیت ارسال شد' )
        return HttpResponseRedirect( request.path_info )

    comments = Comment.objects.get_queryset().filter( product_id=product_id ).order_by(
        '-date_added' ).distinct()  # get comments for current product
    paginator = Paginator( comments, 4 )
    page_number = request.GET.get( 'page' )
    page_obj = paginator.get_page( page_number )

    # get viewer ip adress
    def get_ip(request):
        address = request.META.get( 'HTTP_X_FORWARDED_FOR' )
        if address:
            ip = address.split( ',' )[-1].strip()
        else:
            ip = request.META.get( 'REMOTE_ADDR' )
        return ip

    # find visited count for each product
    ip = get_ip( request )
    visited_ip_product = Visited_Ip_product.objects.filter( product=product, user_ip=ip ).all()
    if len( visited_ip_product ) == 0:
        Visited_Ip_product.objects.create( product=product, user_ip=ip )
        product.visit_count += 1
        product.save()
    context = {
        'title': 'فروشگاه اینترنتی|مشاهده جزئیات محصول',
        'product': product,
        'comments': comments,
        'comment_form': comment_form,
        'paginator': paginator,
        'page_obj': page_obj,
        'grouped_related_products': grouped_related_products,
        'new_order_form': new_order_form
    }
    return render( request, 'products/product_detail.html', context )
