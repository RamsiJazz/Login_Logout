from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.register, name='register'),
    path('loginn', views.loginn, name='loginn'),
    path('signout', views.signout, name='signout'),
]
