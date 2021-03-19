from django import forms
# user order form
from django.contrib.auth.models import User
from django.core import validators
from .models import Province, City, Order


class UserNewOrderForm( forms.Form ):
    product_id = forms.IntegerField( widget=forms.HiddenInput() )
    count = forms.IntegerField( widget=forms.NumberInput( attrs={'id': '¬quantity', 'aria-label': 'Small'} ),
                                initial=1 )


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


class CouponForm( forms.Form ):
    code = forms.CharField( widget=forms.TextInput( attrs={'class': 'form-control', 'type': 'text'} ) )
