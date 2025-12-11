from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Product
from django.contrib.auth import authenticate, login
from django.contrib import messages

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, "shop/product_detail.html", {'product': product})
    return {'categories': Category.objects.all()}   



def admin_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_superuser:
            login(request, user)
            return redirect('admin_dashboard')  # Redirect to your admin dashboard
        else:
            messages.error(request, "Invalid admin credentials!")
            return redirect('admin_login')

    return render(request, "register.html")