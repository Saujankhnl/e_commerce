from datetime import datetime
from django.shortcuts import render, get_object_or_404, redirect
from cart.forms import CartAddProductForm
from shop.forms import CategoryForm
from ecommerce.models import Category  # ✅ correct model
from .models import Product
from django.contrib import messages
from .forms import ProductForm
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required


def register(request):
    if request.method == "POST":
        print(request.POST)
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = request.POST.get("email")
            user.save()
            messages.success(request, "Account created successfully!")
            return redirect("account:user_login")
    else:
        form = CustomUserCreationForm()

    return render(request, "ecommerce/register.html", {"form": form})


@login_required
def home(request):
    """
    Home page view displaying all categories and products
    """
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)

    context = {"categories": categories, "products": products}
    return render(request, "ecommerce/home.html", context)


def product_list(request, category_slug=None):
    """
    Product list view with optional category filtering
    """
    # Get all categories for sidebar - FIXED: This is the key issue
    categories = Category.objects.all()

    # Get all available products - FIXED: Use filter() not all() with arguments
    products = Product.objects.filter(available=True)
    category = None

    # If category slug is provided, filter by it
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = category.products.filter(available=True)

    context = {
        "category": category,
        "products": products,
        "categories": categories,  # FIXED: Ensure categories are always passed
    }
    return render(request, "ecommerce/product_list.html", context)


def product_detail(request, slug):
    """
    Product detail view
    """
    product = get_object_or_404(Product, slug=slug)
    cart_product_form = CartAddProductForm(initial={"quantity": 1, "override": False})

    # FIXED: Also include categories in product detail view if needed in sidebar
    categories = Category.objects.all()

    context = {
        "product": product,
        "cart_product_form": cart_product_form,
        "categories": categories,
    }
    return render(request, "ecommerce/product_detail.html", context)


def add_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            messages.success(
                request,
                f"Category '{category.name}' created successfully in Ecommerce app!",
            )
            return redirect("ecommerce:home")
        else:
            messages.error(
                request, "Category creation failed. Please correct the errors below."
            )
    else:
        form = CategoryForm()

    return render(request, "ecommerce/category_add.html", {"form": form})


def category_detail(request, slug=None):
    """
    If slug is provided → show products for that category.
    If not provided → show all categories.
    """
    categories = Category.objects.all()

    if slug:
        category = get_object_or_404(Category, slug=slug)
        products = Product.objects.filter(category=category, available=True)
    else:
        category = None
        products = Product.objects.filter(available=True)

    context = {
        "category": category,
        "categories": categories,
        "products": products,
    }
    return render(request, "ecommerce/category_detail.html", context)


# FIXED: Remove duplicate function
# def ecommerce_home(request):
#     categories = Category.objects.all()
#     return render(request, "ecommerce/product_list.html", {"categories": categories})


def admin_dashboard(request):
    categories = Category.objects.all()  # From ecommerce app
    products = Product.objects.all()  # From ecommerce app

    context = {
        "categories": categories,
        "products": products,
        "total_sales": 12500.00,  # Replace with actual calculation
        "total_items_sold": 150,  # Replace with actual calculation
        "available_products": products.filter(available=True).count(),
        "year": datetime.now().year,
    }
    return render(request, "admin_dashboard.html", context)


# def add_product_to_category(request, category_slug):
#     category = get_object_or_404(Category, slug=category_slug)

#     if request.method == 'POST':
#         form = ProductForm(request.POST, request.FILES)
#         if form.is_valid():
#             product = form.save(commit=False)
#             product.category = category
#             product.save()
#             return redirect('ecommerce:category_detail', category_slug=category.slug)
#     else:
#         form = ProductForm(initial={'category': category})

#     return render(request, 'ecommerce/add_product.html', {
#         'form': form,
#         'category': category
#     })


def add_product(request):
    """Handle product creation with proper Django form validation"""
    categories = Category.objects.all()

    if request.method == "POST":
        # Use Django form for proper validation and data handling
        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            try:
                product = form.save()
                messages.success(
                    request, f'Product "{product.name}" created successfully!'
                )
                # Redirect to the new product's detail page or product list
                return redirect("ecommerce:product_detail", slug=product.slug)
            except Exception as e:
                messages.error(request, f"Error saving product: {str(e)}")
        else:
            # Form has errors, show them to user
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.title()}: {error}")
    else:
        form = ProductForm()

    return render(
        request, "ecommerce/add_product.html", {"form": form, "categories": categories}
    )


# def products_by_category(request, category_slug):
#     # Fetch category by slug
#     category = get_object_or_404(Category, slug=category_slug)

#     # Fetch products belonging to this category
#     products = Product.objects.filter(category=category, available=True)

#     # Pass to template
#     return render(request, 'products_by_category.html', {
#         'category': category,
#         'products': products,
#     })


def products_by_category(request, category_slug):
    """Show all products under a specific category"""
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category, available=True)

    return render(
        request,
        "products_by_category.html",
        {
            "category": category,
            "products": products,
        },
    )


def category_list(request):
    categories = Category.objects.all()
    print("Category list view accessed")
    return render(request, "ecommerce/category_list.html", {"categories": categories})
