from django.contrib import admin
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "created_at")
    list_filter = ("created_at",)
    prepopulated_fields = {"slug": ("name",)}  # Admin auto-fills slug
    search_fields = ("name", "description")
    ordering = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "stock", "available", "is_in_stock", "created_at")
    list_filter = ("available", "created_at", "updated_at", "category")
    list_editable = ("price", "stock", "available")  # Quick edit in list view
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "description")
    raw_id_fields = ("category",)  # Better for large category lists
    date_hierarchy = "created_at"
    ordering = ("-created_at",)
    
    # Custom method to display in-stock status
    def is_in_stock(self, obj):
        return obj.is_in_stock
    is_in_stock.boolean = True  # Shows nice green/red icons
    is_in_stock.short_description = "In Stock"