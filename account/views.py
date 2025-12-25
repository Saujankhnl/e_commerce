from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Sum
import datetime

from shop.models import Product, Category, Sale


# ==========================
# USER AUTHENTICATION
# ==========================

def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # Redirect admin to admin page
            if user.is_staff:
                return redirect("account:admin_page")

            # Normal user
            return redirect("ecommerce:home")

        messages.error(request, "Invalid credentials!")
        return redirect("account:user_login")

    return render(request, "account/user_login.html")


def logout_view(request):
    logout(request)
    return redirect("account:user_login")


# ==========================
# ADMIN AUTHENTICATION
# ==========================

def is_admin(user):
    return user.is_staff


def admin_login(request):
    # Already logged-in admin

    if request.user.is_authenticated and request.user.is_staff:
        return redirect("account:admin_page")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        remember_me = request.POST.get("remember") == "on"

        if not username or not password:
            messages.error(request, "Please provide username and password.")
            return redirect("account:admin_login")

        user = authenticate(request, username=username, password=password)

        if user and user.is_staff:
            login(request, user)
            response = redirect("account:admin_page")

            # Remember Me cookies
            if remember_me:
                expire_date = datetime.datetime.now() + datetime.timedelta(days=30)
                response.set_cookie("admin_remembered", "true", expires=expire_date)
                response.set_cookie("remembered_username", username, expires=expire_date)
            else:
                response.delete_cookie("admin_remembered")
                response.delete_cookie("remembered_username")

            messages.success(request, f"Welcome Admin, {username}!")
            return response

        messages.error(request, "Invalid admin credentials.")
        return redirect("account:admin_login")

    return render(request, "account/admin_login.html")


# ==========================
# ADMIN DASHBOARD
# ==========================

@login_required(login_url="account:admin_login")
@user_passes_test(is_admin, login_url="account:admin_login")
def admin_page(request):
    # ---------------------------
    # Handle new category creation
    # ---------------------------
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")

        if name:
            Category.objects.create(
                name=name,
                description=description
            )
            messages.success(request, "Category added successfully!")
            return redirect("account:admin_page")
        else:
            messages.error(request, "Category name is required.")

    # ---------------------------
    # Fetch data for dashboard
    # ---------------------------
    products = Product.objects.all()
    categories = Category.objects.all()

    total_products = products.count()
    total_categories = categories.count()

    try:
        total_sales = Sale.objects.aggregate(
            Sum("total_price")
        )["total_price__sum"] or 0

        total_items_sold = Sale.objects.aggregate(
            Sum("quantity")
        )["quantity__sum"] or 0
    except Exception:
        total_sales = 0
        total_items_sold = 0

    recent_products = products.order_by("-id")[:5]

    context = {
        "products": products,
        "categories": categories,
        "total_products": total_products,
        "total_categories": total_categories,
        "total_sales": total_sales,
        "total_items_sold": total_items_sold,
        "recent_products": recent_products,
    }

    return render(request, "account/admin_page.html", context)
# ADMIN LOGOUT
# ==========================

@login_required(login_url="account:admin_login")
def admin_logout(request):
    logout(request)

    response = redirect("account:admin_login")
    response.delete_cookie("admin_remembered")
    response.delete_cookie("remembered_username")

    messages.success(request, "Admin logged out successfully.")
    return response
