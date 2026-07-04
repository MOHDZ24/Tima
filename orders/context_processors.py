from orders.models import Cart


def cart_context(request):
    """Add cart data to all templates."""
    cart = Cart(request)
    return {
        'cart': cart,
        'cart_count': len(cart),
        'cart_total': cart.get_total_price(),
    }
