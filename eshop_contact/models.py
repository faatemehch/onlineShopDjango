from django.db import models


# Create your models here.

class ContactUs( models.Model ):
    user_name = models.CharField( max_length=150, verbose_name='نام کاربری' )
    email = models.EmailField( max_length=150, verbose_name='ایمیل' )
    text = models.TextField( verbose_name='متن پیام' )
    is_read = models.BooleanField( verbose_name='خوانده شده/نشده', default=False )

    def __str__(self):
        return self.user_name

    class Meta:
        verbose_name = 'تماس با ما'
        verbose_name_plural = 'لیست پیام‌های کاربران'

