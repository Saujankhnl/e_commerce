from .cart_manage import Cart

def cart(request):
    return {'cart': Cart(request)}