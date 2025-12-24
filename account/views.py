from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Sum
import datetime
from shop.models import Product, Category, Sale


def logout_view(request):
    print("yes logout")
    logout(request)
    return redirect("account:user_login")


def user_login(request):

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("ecommerce:home")
        else:
            messages.error(request, "Invalid credentials!")
            return redirect("account:user_login")

    return render(request, "account/user_login.html")


def is_admin(user):
    """Check if user is staff/admin"""
    return user.is_staff


def admin_login(request):
    """Handle admin login page"""
    # If user is already authenticated as admin, redirect to dashboard
    if request.user.is_authenticated and request.user.is_staff:
        return redirect("account:admin_dashboard")

    # Check for remember me cookie
    remembered = request.COOKIES.get("admin_remembered")
    if remembered == "true" and request.user.is_authenticated and request.user.is_staff:
        return redirect("account:admin_dashboard")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        remember_me = request.POST.get("remember") == "on"

        if not username or not password:
            messages.error(request, "Please provide both username and password.")
            return redirect("account:register")

        user = authenticate(request, username=username, password=password)
        print(user, user.is_staff)
        if user is not None and user.is_staff:
            login(request, user)

            response = redirect("account:admin_dashboard")

            # Set cookies if remember me is checked
            if remember_me:
                expire_date = datetime.datetime.now() + datetime.timedelta(days=30)
                response.set_cookie("admin_remembered", "true", expires=expire_date)
                response.set_cookie(
                    "remembered_username", username, expires=expire_date
                )
            else:
                response.delete_cookie("admin_remembered")
                response.delete_cookie("remembered_username")

            messages.success(request, f"Welcome back, {username}!")
            return response
        else:
            messages.error(request, "Invalid credentials or not an admin user.")
            return redirect("account:admin_login")

    return render(request, "account/register.html")


@login_required(login_url="account:register")
@user_passes_test(is_admin)
def admin_page(request):
    """Admin dashboard page - requires admin authentication"""
    # Get dashboard statistics
    products = Product.objects.all()
    categories = Category.objects.all()

    # Handle the case where Sale model might not exist
    try:
        total_sales = (
            Sale.objects.aggregate(Sum("total_price"))["total_price__sum"] or 0
        )
        total_items_sold = Sale.objects.aggregate(Sum("quantity"))["quantity__sum"] or 0
    except Exception as e:
        total_sales = 0
        total_items_sold = 0
        print(f"Error calculating sales: {e}")

    # Calculate additional statistics
    total_products = products.count()
    total_categories = categories.count()
    recent_products = products.order_by("-id")[:5]

    context = {
        "products": products,
        "categories": categories,
        "total_sales": total_sales,
        "total_items_sold": total_items_sold,
        "total_products": total_products,
        "total_categories": total_categories,
        "recent_products": recent_products,
    }
    return render(request, "account/admin_page.html", context)


@login_required
def admin_logout(request):
    """Handle admin logout"""
    response = redirect("/")
    response.delete_cookie("admin_remembered")
    response.delete_cookie("remembered_username")
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return response
