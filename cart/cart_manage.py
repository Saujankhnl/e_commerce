# cart/cart.py
from decimal import Decimal
# from django.conf import settings
from ecommerce.models import Product


CART_SESSION_ID = "cart"

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(CART_SESSION_ID)
        if not cart:
            cart = self.session[CART_SESSION_ID] = {}
        self.cart = cart
        

    def add(self, product, quantity=1, override_quantity=False):
        """
        Add a product to the cart or update its quantity.
        Enforces that cart quantity never exceeds product.stock.
        """
        product_id = str(product.id)
        current_qty = self.cart.get(product_id, {}).get("quantity", 0)
        if override_quantity:
            new_qty = quantity
        else:
            new_qty = current_qty + quantity

        # enforce stock limit
        if product.stock is not None:
            if new_qty > product.stock:
                new_qty = product.stock

        self.cart[product_id] = {
            "quantity": int(new_qty),
            "price": str(product.price),
        }
        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        product_ids = list(self.cart.keys())
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        # attach product instances and compute prices
        for product in products:
            item = cart[str(product.id)]
            item["product"] = product
            item["price"] = Decimal(item["price"])
            item["total_price"] = item["price"] * item["quantity"]
        for item in cart.values():
            yield item

    def __len__(self):
        return sum(item["quantity"] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item["price"]) * item["quantity"] for item in self.cart.values())

    def clear(self):
        self.session[CART_SESSION_ID] = {}
        self.save()

    