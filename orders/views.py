from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Cart
from .models import Order, OrderItem
from products.models import Product


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'orders/cart.html', {'cart': cart})


def cart_add(request, product_id):
    product = get_object_or_404(Product, pk=product_id, is_active=True)
    cart = Cart(request)
    quantity = int(request.POST.get('quantity', 1))
    cart.add(product, quantity=quantity)
    messages.success(request, f'تمت إضافة "{product.name}" إلى السلة')
    return redirect('cart_detail')


def cart_remove(request, product_id):
    cart = Cart(request)
    cart.remove(product_id)
    messages.info(request, 'تمت إزالة المنتج من السلة')
    return redirect('cart_detail')


def cart_update(request, product_id):
    if request.method == 'POST':
        cart = Cart(request)
        quantity = int(request.POST.get('quantity', 1))
        cart.update_quantity(product_id, quantity)
    return redirect('cart_detail')


def checkout(request):
    cart = Cart(request)
    if len(cart) == 0:
        messages.warning(request, 'السلة فارغة!')
        return redirect('product_list')

    if request.method == 'POST':
        order = Order.objects.create(
            full_name=request.POST.get('full_name'),
            phone=request.POST.get('phone'),
            phone2=request.POST.get('phone2', ''),
            wilaya=request.POST.get('wilaya'),
            commune=request.POST.get('commune'),
            address=request.POST.get('address'),
            notes=request.POST.get('notes', ''),
            payment_method=request.POST.get('payment_method', 'cod'),
            subtotal=cart.get_total_price(),
            shipping_cost=0,  # Can be calculated based on wilaya
            total=cart.get_total_price(),
        )
        for item in cart:
            OrderItem.objects.create(
                order=order,
                product_name=item['name'],
                product_image=item.get('image', ''),
                price=item['price'],
                quantity=item['quantity'],
            )
        cart.clear()
        messages.success(request, f'تم إنشاء طلبك بنجاح! رقم الطلب: #{order.pk}')
        return redirect('order_success', order_id=order.pk)

    return render(request, 'orders/checkout.html', {'cart': cart})


def order_success(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    return render(request, 'orders/order_success.html', {'order': order})


def order_track(request):
    order = None
    if request.method == 'POST':
        phone = request.POST.get('phone', '').strip()
        order_id = request.POST.get('order_id', '').strip()
        if order_id:
            try:
                order = Order.objects.get(pk=order_id, phone=phone)
            except Order.DoesNotExist:
                messages.error(request, 'لم يتم العثور على الطلب')
        elif phone:
            orders = Order.objects.filter(phone=phone).order_by('-created_at')
            if orders.exists():
                order = orders.first()
            else:
                messages.error(request, 'لم يتم العثور على طبات بهذا الرقم')
    return render(request, 'orders/order_track.html', {'order': order})
