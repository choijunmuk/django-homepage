from django.urls import path

from . import views

app_name = 'hi'

urlpatterns = [

path('', views.index, name='index'),
path('loginsu/', views.loginsu, name='loginsu'),

]