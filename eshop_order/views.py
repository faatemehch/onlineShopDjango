import string
import random
import jdatetime
from zeep import Client
from django.http import Http404
from django.contrib import messages
from django.http import HttpResponse
from eshop_products.models import Product
from .models import Order, OrderDetail, Coupon, City
from django.contrib.auth.decorators import login_required
from .forms import UserNewOrderForm, CouponForm, CompleteOrderForm
from django.shortcuts import render, redirect, HttpResponseRedirect


# create produce tracking code for every new order
def create_ref_code():
    return ''.join( random.choices( string.ascii_lowercase + string.digits, k=20 ) )


# add new item to order, if there is not exist an open order create one
@login_required( login_url='/login' )
def add_user_order(request):
    new_order_form = UserNewOrderForm( request.POST or None )
    if new_order_form.is_valid():
        order: Order = Order.objects.filter( owner_id=request.user.id, is_paid=False ).first()
        # associate tracking code for every new order
        if order is None:
            order = Order.objects.create( owner_id=request.user.id, tracking_code=create_ref_code() )
        product_id = new_order_form.cleaned_data.get( 'product_id' )
        product = Product.objects.get_product_by_id( product_id=product_id )
        count = new_order_form.cleaned_data.get( 'count' )
        # id there exist this item in order its count will be updated else add to order as a new item
        if order.orderdetail_set.filter( product=product ).exists():
            order_item = order.orderdetail_set.filter( product=product, order=order )[0]
            order_item.count += count
            order_item.save()
            messages.success( request, 'سبد خرید برای این محصول بروز شد' )
        else:
            order.orderdetail_set.create( product_id=product_id, price=product.get_price(), count=count )
            messages.success( request, 'این محصول به سبد خرید اضافه شد' )
        # if add an item to order, its quantity will reduce
        product.quantity -= count
        product.save()
        return redirect( "/products/" + str( product.id ) )


# open order for user to check
@login_required( login_url='/login' )
def open_user_order(request):
    context = {
        'order': None,
        'details': None,
        'total': 0,
        'coupon_form': None,
        'title': 'جزئیات سبد خرید'
    }
    coupon_form = CouponForm( request.POST or None )
    open_order: Order = Order.objects.filter( owner_id=request.user.id, is_paid=False ).first()
    if open_order is not None:
        if coupon_form.is_valid() and request.method == 'POST':
            code = coupon_form.cleaned_data.get( 'code' )
            qs_code = Coupon.objects.filter( code=code ).first()  # if entered code is correct or not
            if qs_code is None:
                messages.info( request, 'کد تخفیف وارد شده صحیح نمی‌باشد!' )
            elif open_order.coupon_code is None:
                messages.success( request, 'کد تخفیف با موفقیت اعمال شد' )
                open_order.coupon_code = qs_code
                open_order.use_code = True
                open_order.save()
            elif open_order.use_code is True and open_order.coupon_code.code == code:
                messages.warning( request, 'شما قبلا از این کد تخفیف استفاده کرده‌اید!' )
            else:
                messages.warning( request, 'تنها مجاز به استفاده از یک کد تخفیف می‌باشد!' )
            return HttpResponseRedirect( request.path_info )

        context['coupon_form'] = CouponForm()
        context['order'] = open_order
        context['details'] = open_order.orderdetail_set.all()
        context['total'] = open_order.get_total_price()

    return render( request, 'order/user_open_order.html', context )


# remove an item from order
@login_required( login_url='/login' )
def remove_order_details(request, *args, **kwargs):
    detail_id = kwargs['detail_id']
    if detail_id is not None:
        order_detail = OrderDetail.objects.filter( id=detail_id, order__owner_id=request.user.id ).first()
        order_detail.product.quantity += order_detail.count
        order_detail.product.save()
        order_detail.delete()
        # if order is empty refresh order to default
        order: Order = Order.objects.filter( owner_id=request.user.id, is_paid=False ).first()
        if len( order.orderdetail_set.all() ) == 0:
            order.use_code = False
        order.coupon_code = None
        order.save()
        # messages.success( request, 'محصول مورد نظر از سبد خرید حذف شد!' )
        context = {
            'order': order,
            'details': OrderDetail.objects.filter( order=order ).all(),
            'total': order.get_total_price(),
            'msg': 'محصول مورد نظر از سبد خرید شما حذف شد!',
            'coupon_form': CouponForm()
        }
        return render( request, 'order/change_quantity_orderdetails_ajax.html', context )
    raise Http404


# remove count of an item in order
@login_required( login_url='/login' )
def remove_single_item(request, *args, **kwargs):
    context = {}
    detail_id = kwargs['detail_id']
    if detail_id is not None:
        order_detail = OrderDetail.objects.get_queryset().get( id=detail_id, order__owner_id=request.user.id )
        order_detail.count -= 1
        order_detail.save()
        order_detail.product.quantity += 1
        order_detail.product.save()
        order: Order = Order.objects.filter( owner_id=request.user.id, is_paid=False ).first()
        context['order'] = order
        context['details'] = order.orderdetail_set.all()
        context['total'] = order.get_total_price()
        context['coupon_form'] = CouponForm()
    if order_detail.count == 0:
        order_detail.delete()
        # if order is empty refresh order to default
        if len( order.orderdetail_set.all() ) == 0:
            order.use_code = False
            order.coupon_code = None
            order.save()
        # messages.success( request, 'محصول مورد نظر از سبد خرید حذف شد!' )
    # return redirect( 'open_user_order' )
    return render( request, 'order/change_quantity_orderdetails_ajax.html', context )


# add count of an item in open order
@login_required( login_url='/login' )
def add_single_item(request, *args, **kwargs):
    detail_id = kwargs['detail_id']
    context = {}
    if detail_id is not None:
        order: Order = Order.objects.filter( owner_id=request.user.id, is_paid=False ).first()
        order_detail = OrderDetail.objects.get_queryset().get( id=detail_id, order__owner_id=request.user.id )
        if order_detail.product.quantity > 0:
            order_detail.count += 1
            order_detail.product.quantity -= 1
            order_detail.product.save()
            context['order'] = order
            context['details'] = order.orderdetail_set.all()
            context['total'] = order.get_total_price()
            context['coupon_form'] = CouponForm()
        else:
            context['order'] = order
            context['details'] = order.orderdetail_set.all()
            context['total'] = order.get_total_price()
            context['coupon_form'] = CouponForm()
            context['msg'] = 'تعداد سفارش محصول بیش از حد مجاز است!'
        order_detail.save()
        # return redirect( 'open_user_order' )
        return render( request, 'order/change_quantity_orderdetails_ajax.html', context )


# load cities based on province with ajax
def load_cities(request):
    province_id = request.GET.get( 'province' )
    cities = City.objects.filter( province_id=province_id ).order_by( 'city_name' )
    context = {'cities': cities}
    return render( request, 'order/cities_dropdown.html', context )


# complete order process
@login_required( login_url='/login' )
def complete_order(request):
    complete_form = CompleteOrderForm( request.POST or None )
    print( complete_form.fields )
    if complete_form.is_valid() and complete_form.cleaned_data.items() is not None:
        # cleaned data
        f_name = complete_form.cleaned_data.get( 'name' )
        family = complete_form.cleaned_data.get( 'family' )
        phone_number = complete_form.cleaned_data.get( 'phone_number' )
        post_code = complete_form.cleaned_data.get( 'post_code' )
        province = complete_form.cleaned_data.get( 'province' )
        city = complete_form.cleaned_data.get( 'city' )
        address = complete_form.cleaned_data.get( 'address' )
        descriptions = complete_form.cleaned_data.get( 'description' )
        order = Order.objects.filter( is_paid=False, owner_id=request.user.id ).first()
        # complete user order
        order.name = f_name
        order.family = family
        order.phone_number = phone_number
        order.post_code = post_code
        order.province = province
        order.city = city
        order.address = address
        order.description = descriptions
        order.is_paid = True
        order.payment_date = jdatetime.datetime.now()
        order.save()
        orderDetails = OrderDetail.objects.filter( order=order ).all()
        for detail in orderDetails:
            detail.product.sell_count += detail.count
            detail.product.save()
        messages.success( request, 'پرداخت شما با موفقیت انجام شد' )
        return redirect( 'request' )
    context = {
        'title': 'تکمیل فرآیند خرید',
        'complete_form': complete_form
    }
    return render( request, 'order/complete_order.html', context )


# add new item into open order from product list view
@login_required( login_url='/login' )
def add_single_new_item_from_product_list(request, *args, **kwargs):
    product_id = kwargs['product_id']
    if product_id is not None:
        product = Product.objects.get_product_by_id( product_id )
        user_order: Order = Order.objects.filter( owner_id=request.user.id, is_paid=False ).first()
        if user_order is None:
            user_order: Order = Order.objects.create( owner_id=request.user.id, is_paid=False,
                                                      tracking_code=create_ref_code() )
        order_detail = OrderDetail.objects.get_queryset().filter( product=product, order=user_order ).first()
        if order_detail is not None:
            order_detail.count += 1
            product.quantity -= 1
            product.save()
            order_detail.save()
        else:
            order_detail = user_order.orderdetail_set.create( product=product, count=1, price=product.get_price() )
            product.quantity -= 1
            product.save()
            order_detail.save()
        messages.success( request, 'محصول مورد نظر به سبد خرید افزوده شد!' )
        return HttpResponseRedirect( request.META.get( 'HTTP_REFERER' ) )


# show all user orders
@login_required( login_url='/login' )
def show_all_user_orders(request):
    context = {
        'title': 'مشاهده سفارشات کاربر',
        'user_orders': Order.objects.filter( owner_id=request.user.id, is_paid=True ).all().order_by( '-payment_date' )
    }
    return render( request, 'order/all_user_orders.html', context )


# one order details for one user
# change order from un-send to sent with ajax
@login_required( login_url='/login' )
def change_to_send_order(request, *args, **kwargs):
    user_order = Order.objects.filter( id=kwargs['order_id'], is_paid=True ).first()
    if user_order.is_send:
        user_order.is_send = False
        user_order.save()
    else:
        user_order.is_send = True
        user_order.save()
    context = {'user_order': user_order}
    return render( request, 'order/user_single_order_details.html', context )


# orders for all users
# show details of a payed order
@login_required( login_url='/login' )
def show_user_order_detail(request, *args, **kwargs):
    if request.user.is_superuser:
        user_order = Order.objects.filter( is_paid=True, id=kwargs['user_order_id'] ).first()
    else:
        user_order = Order.objects.filter( owner_id=request.user.id, is_paid=True, id=kwargs['user_order_id'] ).first()
    context = {
        'title': 'مشاهده جزئیات سفارش',
        'user_order': user_order,
    }
    return render( request, 'order/user_single_order_details.html', context )


# show send and un-send orders with ajax
@login_required( login_url='/login' )
def load_get_sent_order(request, *args, **kwargs):
    value = kwargs['value']
    context = {}
    if value == 'True':
        orders = Order.objects.filter( is_paid=True, is_send=True ).all().order_by( 'payment_date' )
        context['inner_title'] = 'مشاهده سفارشات ارسال نشده'
        context['value'] = 'False'
    else:
        orders = Order.objects.filter( is_paid=True, is_send=False ).all().order_by( 'payment_date' )
        context['inner_title'] = 'مشاهده سفارشات ارسال شده'
        context['value'] = 'True'
    context['users_order'] = orders
    return render( request, 'order/load_sent_unsend_orders.html', context )


# all paid orders view
@login_required( login_url='/login' )
def order_user_view(request):
    if request.user.is_superuser:
        users_order = Order.objects.filter( is_paid=True, is_send=False ).all().order_by( '-payment_date' )
        context = {'users_order': users_order,
                   'inner_title': 'مشاهده سفارشات ارسال شده',
                   'value': True
                   }
        return render( request, 'order/order_user_view_from_admin.html', context )
    else:
        return render( request, '404.html' )


MERCHANT = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'
client = Client( 'https://www.zarinpal.com/pg/services/WebGate/wsdl' )
amount = 1000  # Toman / Required
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
email = 'email@example.com'  # Optional
mobile = '09123456789'  # Optional
CallbackURL = 'http://localhost:8000/verify/'  # Important: need to edit for realy server.


@login_required( login_url='/login' )
def send_request(request, *args, **kwargs):
    total_price = 0
    open_order: Order = Order.objects.filter( is_paid=False, owner_id=request.user.id ).first()
    if open_order is not None:
        total_price = open_order.get_total_price()
        result = client.service.PaymentRequest( MERCHANT, total_price, description, email, mobile,
                                                f'{CallbackURL}/{open_order.id}', )
        if result.Status == 100:
            return redirect( 'https://www.zarinpal.com/pg/StartPay/' + str( result.Authority ) )
        else:
            return HttpResponse( 'Error code: ' + str( result.Status ) )
    raise Http404()


@login_required( login_url='/login' )
def verify(request, *args, **kwargs):
    order_id = kwargs.get( 'order_id' )
    if request.GET.get( 'Status' ) == 'OK':
        result = client.service.PaymentVerification( MERCHANT, request.GET['Authority'], amount )
        if result.Status == 100:
            user_order = Order.objects.get_queryset().get( id=order_id )
            user_order.is_paid = True
            user_order.payment_date = jdatetime.datetime.now()
            user_order.save()
            return HttpResponse( 'Transaction success.\nRefID: ' + str( result.RefID ) )
        elif result.Status == 101:
            return HttpResponse( 'Transaction submitted : ' + str( result.Status ) )
        else:
            return HttpResponse( 'Transaction failed.\nStatus: ' + str( result.Status ) )
    else:
        return HttpResponse( 'Transaction failed or canceled by user' )
