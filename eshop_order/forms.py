from django import forms
# user order form
from django.contrib.auth.models import User
from django.core import validators


class UserNewOrderForm( forms.Form ):
    product_id = forms.IntegerField( widget=forms.HiddenInput() )
    count = forms.IntegerField( widget=forms.NumberInput( attrs={'id': '¬quantity', 'aria-label': 'Small'} ),
                                initial=1 )


# CITY_CHOICES = (
#     ('0', 'لطفا استان را انتخاب نمایید')
# )
#
# PROVINCE_CHOICES = (
#     ('0', 'لطفا استان را انتخاب نمایید'),
#     ('1', 'تهران'),
#     ('2', 'گیلان'),
#     ('3', 'آذربایجان شرقی'),
#     ('4', 'خوزستان'),
#     ('5', 'فارس'),
#     ('6', 'اصفهان'),
#     ('7', 'خراسان رضوی'),
#     ('8', 'قزوین'),
#     ('9', 'سمنان'),
#     ('10', 'قم'),
#     ('11', 'مرکزی'),
#     ('12', 'زنجان'),
#     ('13', 'مازندران'),
#     ('14', 'گلستان'),
#     ('15', 'اردبیل'),
#     ('16', 'آذربایجان غربی'),
#     ('17', 'همدان'),
#     ('18', 'کردستان'),
#     ('19', 'کرمانشاه'),
#     ('20', 'لرستان'),
#     ('21', 'بوشهر'),
#     ('22', 'کرمان'),
#     ('23', 'هرمزگان'),
#     ('24', 'چهارمحال و بختیاری'),
#     ('25', 'یزد'),
#     ('26', 'سیستان و بلوچستان'),
#     ('27', 'ایلام'),
#     ('28', 'کهگلویه و بویراحمد'),
#     ('29', 'خراسان شمالی'),
#     ('30', 'خراسان جنوبی'),
#     ('31', 'البرز')
# )

from .models import Province, City, Order


class CompleteOrderForm( forms.ModelForm ):
    class Meta:
        model = Order
        fields = (
            'name',
            'family',
            'phone_number',
            'post_code',
            'province',
            'city',
            'address',
            'description'
        )
        widgets = {
            'name': forms.TextInput( attrs={'class': 'form-control', 'placeholder': 'نام'} ),
            'family': forms.TextInput( attrs={'class': 'form-control', 'placeholder': 'نام‌خانوادگی'} ),
            'post_code': forms.NumberInput( attrs={'class': 'form-control', 'placeholder': '1234567'} ),
            'phone_number': forms.NumberInput( attrs={'class': 'form-control', 'placeholder': '09123456789'} ),
            'province': forms.Select( attrs={'class': 'form-control'} ),
            'city': forms.Select( attrs={'class': 'form-control'} ),
            'address': forms.Textarea( attrs={'class': 'form-control', 'row': '5', 'value': '0'} ),
            'description': forms.Textarea( attrs={'class': 'form-control', 'row': '5'} )

        }
        labels = {
            'name': 'نام',
            'family': 'نام‌خانوادگی',
            'phone_number': 'تلفن همراه',
            'post_code': 'کد پستی',
            'province': 'استان',
            'city': 'شهر',
            'address': 'آدرس',
            'description': 'توضیحات'
        }

        def __init__(self, *args, **kwargs):
            super().__init__( *args, **kwargs )
            self.fields['city'].queryset = City.objects.none()
            self.fields['description'].required = False

            if 'province' in self.data:
                try:
                    province_id = int( self.data.get( 'province' ) )
                    self.fields['city'].queryset = City.objects.filter( province_id=province_id ).order_by(
                        'city_name' )
                except (ValueError, TypeError):
                    pass  # invalid input from the client; ignore and fallback to empty City queryset
            elif self.instance.pk:
                self.fields['city'].queryset = self.instance.province.city_set.order_by( 'city_name' )


#     f_name = forms.CharField(
# class CompleteOrderForm( forms.Form ):
#         widget=forms.TextInput( attrs={'class': 'form-control', 'placeholder': 'نام'} ), label='نام:' )
#         widget=forms.TextInput( attrs={'class': 'form-control', 'placeholder': 'نام‌خانوادگی'} ),
#     l_name = forms.CharField(
#         label='نام‌خانوادگی:' )
#         widget=forms.NumberInput( attrs={'class': 'form-control', 'placeholder': '09123456789'} ), label='تلفن همراه:' )
#     phone_number = forms.CharField(
#     post_code = forms.CharField(
#     province = forms.ChoiceField(
#         widget=forms.NumberInput( attrs={'class': 'form-control', 'placeholder': '1234567'} ), label='کد پستی:' )
#         widget=forms.Select( attrs={'class': 'form-control', 'onChange': 'iranwebsv(this.value)'} ),
#     city = forms.ChoiceField(
#         label='انتخاب استان:', choices=PROVINCE_CHOICES )
#         widget=forms.Select( attrs={'class': 'form-control', 'id': 'city', 'name': 'city', 'value': '0'} ),
#     address = forms.CharField( widget=forms.Textarea( attrs={'class': 'form-control', 'row': '5', 'value': '0'} ),
#         label='انتخاب شهر:' )
#                                label='آدرس دقیق:' )
#     description = forms.CharField( widget=forms.Textarea( attrs={'class': 'form-control', 'row': '5'} ),
#                                    label='توضیحات:', required=False )


class CouponForm( forms.Form ):
    code = forms.CharField( widget=forms.TextInput( attrs={'class': 'form-control', 'type': 'text'} ) )
