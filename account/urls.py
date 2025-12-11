from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('admin_page/', views.admin_page, name='admin_page'),
    
]