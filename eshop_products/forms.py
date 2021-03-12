from django.core import validators
from django import forms


class CommentForm( forms.Form ):
    full_name = forms.CharField(
        widget=forms.TextInput(
            attrs={'placeholder': 'نام و نام خانوادگی خود را وارد نمایید', 'class': 'form-control'} ),
        label='نام و نام خانوادگی',
        validators=[validators.MaxLengthValidator( 120, 'نام و نام خانوادگی شما نمی‌تواند بیش از ۱۵۰ کاراکتر باشد' )] )
    email = forms.EmailField(
        widget=forms.EmailInput( attrs={'placeholder': 'ایمیل خود را وارد نمایید', 'class': 'form-control'} ),
        label='ایمیل',
        validators=[validators.MaxLengthValidator( 100, 'ایمیل شما نمی‌تواند بیش از ۱۰۰ کاراکتر باشد' )] )
    comment = forms.CharField(
        widget=forms.Textarea(
            attrs={'placeholder': 'متن نظر خود را نسبت به این کالا وارد نمایید', 'class': 'form-control',
                   'id': 'comment-text-input', 'cols': 80} ),
        label='متن نظر' )

    # choices_comment = forms.ChoiceField( widget=forms.Select(),
    #                                      label='رای شما به این محصول', choices=CHOICES, required=False )
