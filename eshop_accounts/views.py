from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import LoginForm, RegisterForm, EditUserAccountForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.models import Group


# register & login $ logout views

# login user if there exist
def login_view(request):
    if request.user.is_authenticated:
        return redirect( 'home' )
    login_form = LoginForm( request.POST or None )
    if login_form.is_valid():
        user_name = login_form.cleaned_data.get( 'user_name' )
        password = login_form.cleaned_data.get( 'password' )
        user = authenticate( request, username=user_name, password=password )
        if user is not None:  # if user is exist
            login( request, user )
            messages.success( request, 'به فروشگاه اینترنتی ما خوش آمدید!' )
            return redirect( 'home' )
        else:  # if user does not exist
            login_form.add_error( 'user_name', 'کاربری با مشخصات وارد شده وجود ندارد!' )
    context = {
        'title': 'صفحه ورود به سایت',
        'login_form': login_form
    }
    return render( request, 'account/login_page.html', context )


# register new user if does not exist
def register_view(request):
    if request.user.is_authenticated:
        return redirect( 'home' )
    register_form = RegisterForm( request.POST or None )
    if register_form.is_valid():
        user_name = register_form.cleaned_data.get( 'user_name' )
        email = register_form.cleaned_data.get( 'email' )
        password = register_form.cleaned_data.get( 'password' )
        re_password = register_form.cleaned_data.get( 're_password' )
        user = User.objects.create_user( username=user_name, email=email, password=password )
        group = Group.objects.get( name='مشتریان' )
        group.user_set.add( user )
        user.save()
        messages.success( request, 'ثبت نام با موفقیت انجام شد. می‌توانید وارد شوید!' )
        return redirect( 'login' )
    context = {
        'title': 'ثبت نام در سایت',
        'register_form': register_form
    }
    return render( request, 'account/register_page.html', context )


# logout user
def logout_user(request):
    logout( request )
    messages.success( request, 'عملیات خروج از سایت با موفقیت انجام شد!' )
    return redirect( 'login' )


# edit user account
@login_required( login_url='/login' )
def edit_user_account(request):
    edit_account_form = EditUserAccountForm( request.POST or None )
    print( edit_account_form.is_valid() )
    if edit_account_form.is_valid():
        f_name = edit_account_form.cleaned_data.get( 'f_name' )
        l_name = edit_account_form.cleaned_data.get( 'l_name' )
        email = edit_account_form.cleaned_data.get( 'email' )
        user: User = User.objects.filter( username=request.user.username ).first()
        user.first_name = f_name
        user.last_name = l_name
        user.email = email
        user.save()
        messages.success( request, 'تغییرات با موفقیت اعمال شد!' )
        return redirect( 'home' )

    context = {
        'title': 'فروشگاه اینترنتی|ویرایش حساب کاربری',
        'edit_account_form': edit_account_form
    }
    return render( request, 'account/edit_user_account.html', context )
