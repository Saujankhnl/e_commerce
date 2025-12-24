from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
   
    path('admin_page/', views.admin_page, name='admin_page'),
    path('admin_login/', views.admin_login, name='admin_login'),
    path('user_login/',views.user_login,name='user_login'),
]