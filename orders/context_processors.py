from orders.models import Cart
from core.models import SiteSettings


def cart_context(request):
    """Add cart data to all templates."""
    cart = Cart(request)
    site_settings = SiteSettings.load()
    return {
        'cart': cart,
        'cart_count': len(cart),
        'cart_total': cart.get_total_price(),
        'site_settings': site_settings,
    }
