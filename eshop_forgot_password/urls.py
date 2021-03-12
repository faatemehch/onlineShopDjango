from django.urls import path
from django.contrib.auth import views as forogot_password_view

urlpatterns = [
    path( 'password-reset/', forogot_password_view.PasswordResetView.as_view(
        template_name='forgot_password/password_reset_form.html',
        email_template_name='forgot_password/password_reset_email.html',
        subject_template_name='forgot_password/password_reset_subject.txt'
    ), name='password_reset' ),

    path( 'password-reset/done/', forogot_password_view.PasswordResetDoneView.as_view(
        template_name='forgot_password/password_reset_done.html'
    ),
          name='password_reset_done' ),

    path( 'password-reset-confirm/<uidb64>/<token>/',
          forogot_password_view.PasswordResetConfirmView.as_view(
              template_name='forgot_password/password_reset_confirm.html'
          ),
          name='password_reset_confirm' ),

    path( 'password-reset-complete/',
          forogot_password_view.PasswordResetCompleteView.as_view(
              template_name='forgot_password/password_reset_complete.html'
          ),
          name='password_reset_complete' ),
]
