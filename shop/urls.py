from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
]
