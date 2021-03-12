from django.urls import path
from .views import contact_page
urlpatterns = [
    path('contact_us', contact_page, name='contact_us')
]
