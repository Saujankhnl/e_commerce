from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.http import require_POST
from ecommerce.models import Product
from .cart_manage import Cart
from .forms import CartAddProductForm
# from cart.forms import CartAddProductForm

@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity=cd["quantity"], override_quantity=cd["override"])
    return redirect("cart:cart_detail")

def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect("cart:cart_detail")

def cart_detail(request):
    cart = Cart(request)
    return render(request, "cart/cart_detail.html", {"cart": cart})

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, available=True)
    cart_product_form = CartAddProductForm()
    return render(request, "ecommerce/product_detail.html", {
        "product": product,
        "cart_product_form": cart_product_form,
    })

def cart_update(request):
    # cart = Cart(request)
    return render(request, "cart/cart_update.html")