from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import ContactUsForm
from .models import ContactUs
from eshop_settings.models import SiteSetting


# contact page view
def contact_page(request):
    # , initial={'user_name': request.user.username}
    contact_form = ContactUsForm( request.POST or None )
    if contact_form.is_valid():
        if request.user.is_authenticated:  # creat new contact model if user have been logged in
            user_name = contact_form.cleaned_data.get( 'user_name' )
            email = contact_form.cleaned_data.get( 'email' )
            text = contact_form.cleaned_data.get( 'text' )
            ContactUs.objects.create( user_name=user_name, email=email, text=text )
            messages.success( request, 'پیام شما با موفقیت ارسال شد!' )
            return HttpResponseRedirect( request.path_info )
        else:
            messages.warning( request, 'ابتدا باید وارد سایت شوید!' )
            return redirect( 'login' )
    contact_form = ContactUsForm()
    context = {
        'title': 'فروشگاه اینترنتی|تماس با ما',
        'contact_form': contact_form,
        'settings': SiteSetting.objects.last()
    }
    return render( request, 'contact_us/contact_us_page.html', context )
