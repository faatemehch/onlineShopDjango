from django import forms
from captcha.fields import CaptchaField
from django.contrib.auth.models import User
from django.core import validators


# login form
class LoginForm( forms.Form ):
    user_name = forms.CharField( widget=forms.TextInput( attrs={
        'placeholder': 'نام کاربری', 'class': 'form-control'
    } ), label='نام کاربری', required=True,
        validators=
        [validators.MaxLengthValidator( limit_value=20,
                                        message='تعداد کاراکتر‌های وارد شده از ۲۰ کاراکتر نمی‌تواند بیشتر باشد!' )
         ] )

    password = forms.CharField( widget=forms.PasswordInput( attrs={
        'placeholder': 'رمز عبور', 'class': 'form-control'
    } ), label='رمز عبور', required=True )

    captcha = CaptchaField( label='' )

    def clean_user_name(self):
        user_name = self.cleaned_data.get( 'user_name' )
        is_exist_user = User.objects.filter( username=user_name ).exists()
        if not is_exist_user:
            raise forms.ValidationError( 'کاربری با این نام وجود ندارد!' )
        return user_name

    # def clean_password(self):
    #     user_name = self.cleaned_data.get( 'user_name' )
    #     password = self.cleaned_data.get( 'password' )
    #     is_exist_user = User.objects.filter( username=user_name, password=password ).exists()
    #     print( is_exist_user )
    #     if not is_exist_user:
    #         raise forms.ValidationError( 'کلمه عبور برای کاربر وارد شده صحیح نمی‌باشد!' )
    #     return password


# register form
class RegisterForm( forms.Form ):
    user_name = forms.CharField( widget=forms.TextInput( attrs={
        'placeholder': 'نام کاربری', 'class': 'form-control'
    } ), label='نام کاربری', required=True, validators=
    [validators.MaxLengthValidator( limit_value=20,
                                    message='تعداد کاراکتر‌های وارد شده از ۲۰ کاراکتر نمی‌تواند بیشتر باشد!' )
     ] )

    email = forms.EmailField( widget=forms.EmailInput( attrs={
        'placeholder': 'ایمیل', 'class': 'form-control'
    } ), label='ایمیل', required=True, validators=
    [validators.MaxLengthValidator( limit_value=30,
                                    message='تعداد کاراکتر‌های وارد شده از ۳۰ کاراکتر نمی‌تواند بیشتر باشد!' )
     ] )

    password = forms.CharField( widget=forms.PasswordInput( attrs={
        'placeholder': 'کلمه عبور', 'class': 'form-control'
    } ), label='کلمه عبور', required=True )

    re_password = forms.CharField( widget=forms.PasswordInput( attrs={
        'placeholder': 'تکرار کلمه عبور', 'class': 'form-control'
    } ), label='تکرار کلمه عبور', required=True )

    def clean_user_name(self):
        user_name = self.cleaned_data.get( 'user_name' )
        is_exist_user = User.objects.filter( username=user_name ).exists()
        if is_exist_user:
            raise forms.ValidationError( 'کاربری با این نام قبلا ثبت نام کرده است!' )
        return user_name

    def clean_email(self):
        email = self.cleaned_data.get( 'email' )
        is_exist_email = User.objects.filter( email=email ).exists()
        if is_exist_email:
            raise forms.ValidationError( 'ایمبل خود را تغییر دهید!' )
        return email

    def clean_re_password(self):
        password = self.cleaned_data.get( 'password' )
        re_password = self.cleaned_data.get( 're_password' )
        if password != re_password:
            raise forms.ValidationError( 'کلمه عبور و تکرار آن باهم مطابقت ندارند!' )
        return re_password


class EditUserAccountForm( forms.Form ):
    f_name = forms.CharField(
        widget=forms.TextInput( attrs={'class': 'form-control', 'placeholder': 'نام'} ), label='نام:', validators=
        [validators.MaxLengthValidator( limit_value=20,
                                        message='تعداد کاراکتر‌های وارد شده از ۲۰ کاراکتر نمی‌تواند بیشتر باشد!' )
         ] )
    l_name = forms.CharField(
        widget=forms.TextInput( attrs={'class': 'form-control', 'placeholder': 'نام‌خانوادگی'} ),
        label='نام‌خانوادگی:', validators=
        [validators.MaxLengthValidator( limit_value=20,
                                        message='تعداد کاراکتر‌های وارد شده از ۲۰ کاراکتر نمی‌تواند بیشتر باشد!' )
         ] )

    email = forms.EmailField( widget=forms.EmailInput( attrs={
        'placeholder': 'ایمیل', 'class': 'form-control'
    } ), label='ایمیل', required=True, validators=
    [validators.MaxLengthValidator( limit_value=30,
                                    message='تعداد کاراکتر‌های وارد شده از ۳۰ کاراکتر نمی‌تواند بیشتر باشد!' )
     ] )

    # phone_number = forms.CharField(
    #     widget=forms.NumberInput( attrs={'class': 'form-control', 'placeholder': '09123456789'} ), label='تلفن همراه:',
    #     validators=[validators.MaxLengthValidator(
    #         limit_value=11, message='تعداد کاراکتر‌های وارد شده از ۱۱ کاراکتر نمی‌تواند بیشتر باشد!' )
    #     ] )

    def clean_email(self):
        email = self.cleaned_data.get( 'email' )
        is_exist_email = User.objects.filter( email=email ).exists()
        if is_exist_email:
            raise forms.ValidationError( 'ایمبل دیگری وارد کنید!' )
        return email