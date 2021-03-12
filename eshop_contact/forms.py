from django import forms
from django.core import validators


class ContactUsForm( forms.Form ):
    user_name = forms.CharField( widget=forms.TextInput(
        attrs={'placeholder': 'نام کاربری', 'class': 'form-control'} ), label='نام کاربری', validators=[
        validators.MaxLengthValidator( 5, 'نام کاربری شما نمی‌تواند بیش‌ از ۱۵۰ کاراکتر باشد!' )
    ]
    )
    email = forms.EmailField( widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'ایمیل'} ), label='ایمیل', validators=[
        validators.MaxLengthValidator( 150, 'ایمیل شما نمی‌تواند بیش‌ از ۱۵۰ کاراکتر باشد!' )
    ]
    )
    text = forms.CharField( widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': 'متن پیام', 'row': '7', 'id': 'textMessage'} ), label='متن پیام'
    )
