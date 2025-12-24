from django.urls import path
from . import views

app_name = "ecommerce"

urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    # Category list page
    path("category_list/", views.category_list, name="category_list"),
    # Add new category
    path("add-category/", views.add_category, name="add_category"),
    # Category detail page (view all products under a category)
    path("category/<slug:slug>/", views.category_detail, name="category_detail"),
    # Product listing (optionally filter by category)
    path("products/", views.product_list, name="product_list"),
    path(
        "products/category/<slug:category_slug>/",
        views.products_by_category,
        name="products_by_category",
    ),
    # Product detail
    path("product/<slug:slug>/", views.product_detail, name="product_detail"),
    # Add product
    path("add-product/", views.add_product, name="add_product"),
]
