from django.conf.urls import url
from basic_app import views
from django.urls import path
from django.contrib import admin

app_name = 'basic_app'
urlpatterns = [
    path('register/',views.register,name='register'),
    path('user_logn/',views.user_login,name='user_login')
]
