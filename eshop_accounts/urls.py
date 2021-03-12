from django.urls import path, include
from .views import login_view, register_view, logout_user, edit_user_account

urlpatterns = [
    path( 'login', login_view, name='login' ),
    path( 'register', register_view, name='register' ),
    path( 'logout', logout_user, name='logout' ),
    path( 'edit_user_account', edit_user_account, name='edit_user_account' ),

]
