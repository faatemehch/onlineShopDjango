from django.urls import path
from .views import home_page, about_page
from django.conf.urls import handler404

urlpatterns = [
    path( '', home_page, name='home' ),
    path( 'about_us', about_page, name='about_us' ),
]

handler404 = 'eshop_settings.views.handler404'
