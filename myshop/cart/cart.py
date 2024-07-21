from decimal import Decimal
from django.conf import settings
from shop.models import Product

class Cart:
    def __init__(self, request):
        """
        Initialize the cart.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, override_quantity=False):
        """
        Añadir un producto al carrito o modificar su cantidad
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,
                                     'price': str(product.price)}
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()
        
    def remove(self, product):
        """
        Eliminar un producto del carrito.
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()
    
    def __iter__(self):
        """
        Itera sobre todos los productos del carrito en la base de datos.
        """
        product_ids = self.cart.keys()
        # get the product objects and add them to the cart
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item
    
    def __len__(self):
        """
        Cuenta el número de elementos en el carrito.
        """
        return sum(item['quantity'] for item in self.cart.values())
    
    def get_total_price(self):
        """
        Calcula el precio total del carrito.
        """
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())
    
    def clear(self):
        """
        Vacía el carrito de sesión
        """
        del self.session[settings.CART_SESSION_ID]
        self.save()
        
    def save(self):
        # para que los cambios se queden guardados en la sesión
        self.session.modified = True