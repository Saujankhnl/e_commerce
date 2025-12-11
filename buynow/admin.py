from django.contrib import admin
from .models import Product, Sale

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity')

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'total_price', 'payment_method', 'date')
    list_filter = ('payment_method', 'date')
    search_fields = ('product__name',)