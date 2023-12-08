from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',home,name="home"),
    path('write_review/<int:id>/',write_review,name="write_review"),
    path('login/',login,name='login'),
    path('sign-up/',sign_up,name="sign-up"),
    path('logout/',logout,name="logout"),
    path('verify/<str:token>/',verify,name="verify"),
    
    # Foret Password
    path('password_reset/',auth_views.PasswordResetView.as_view(template_name = 'password_reset_form.html'),name='password_reset'),
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(template_name = 'password_reset_done.html'),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name = 'password_reset_confirm.html'),name='password_reset_confirm'),
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(template_name = 'password_reset_complete.html'),name='password_reset_complete'),
]