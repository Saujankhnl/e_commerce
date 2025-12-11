from django.shortcuts import render, redirect
from .models import Product, Sale
from django.contrib import messages

def buy_now(request):
    product = Product.objects.first()  # Example: get first product
    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        quantity = int(request.POST.get('quantity', 1))

        if product and product.quantity >= quantity:
            total_price = product.price * quantity

            # Save sale record
            Sale.objects.create(
                product=product,
                quantity=quantity,
                total_price=total_price,
                payment_method=payment_method
            )

            # Reduce stock
            product.quantity -= quantity
            product.save()

            messages.success(request, f"Order successful via {payment_method}!")
            return redirect('buynow:buy_now')
        else:
            messages.error(request, "Not enough stock available.")

    return render(request, 'buynow/buy_now.html', {'product': product})
