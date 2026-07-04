from django.db import models
from django.conf import settings


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'قيد الانتظار'),
        ('confirmed', 'تم التأكيد'),
        ('shipped', 'تم الشحن'),
        ('delivered', 'تم التوصيل'),
        ('cancelled', 'ملغي'),
    ]

    PAYMENT_CHOICES = [
        ('cod', 'الدفع عند الاستلام'),
        (' ccp', 'تحويل CCP'),
        ('baridi', 'باريدي موب'),
    ]

    # Customer info
    full_name = models.CharField('الاسم الكامل', max_length=200)
    phone = models.CharField('رقم الهاتف', max_length=20)
    phone2 = models.CharField(
        'رقم هاتف ثاني', max_length=20, blank=True
    )
    wilaya = models.CharField('الولاية', max_length=100)
    commune = models.CharField('البلدية', max_length=100)
    address = models.TextField('العنوان')
    notes = models.TextField('ملاحظات', blank=True)

    # Order info
    status = models.CharField(
        'الحالة', max_length=20, choices=STATUS_CHOICES, default='pending'
    )
    payment_method = models.CharField(
        'طريقة الدفع', max_length=20, choices=PAYMENT_CHOICES, default='cod'
    )
    subtotal = models.DecimalField('المجموع الفرعي', max_digits=10, decimal_places=2, default=0)
    shipping_cost = models.DecimalField('تكلفة الشحن', max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField('المجموع الكلي', max_digits=10, decimal_places=2, default=0)

    # Tracking
    tracking_number = models.CharField('رقم التتبع', max_length=100, blank=True)
    created_at = models.DateTimeField('تاريخ الطلب', auto_now_add=True)
    updated_at = models.DateTimeField('تاريخ التحديث', auto_now=True)

    class Meta:
        verbose_name = 'طلب'
        verbose_name = 'طلبات'
        ordering = ['-created_at']

    def __str__(self):
        return f'طلب #{self.pk} - {self.full_name}'

    def get_absolute_url(self):
        return f'/order/{self.pk}/'


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE,
        related_name='items', verbose_name='الطلب'
    )
    product_name = models.CharField('اسم المنتج', max_length=300)
    product_image = models.CharField('صورة المنتج', max_length=500, blank=True)
    price = models.DecimalField('السعر', max_digits=10, decimal_places=2)
    quantity = models.IntegerField('الكمية', default=1)

    class Meta:
        verbose_name = 'عنصر طلب'
        verbose_name = 'عناصر الطلب'

    def __str__(self):
        return f'{self.product_name} x{self.quantity}'

    @property
    def total_price(self):
        return self.price * self.quantity


class Cart:
    """Session-based shopping cart."""

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1):
        product_id = str(product.pk)
        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.price),
                'name': product.name,
                'image': product.image.url if product.image else '',
            }
        self.cart[product_id]['quantity'] += quantity
        self.save()

    def remove(self, product_id):
        product_id = str(product_id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def update_quantity(self, product_id, quantity):
        product_id = str(product_id)
        if product_id in self.cart:
            self.cart[product_id]['quantity'] = quantity
            if quantity <= 0:
                self.remove(product_id)
            self.save()

    def save(self):
        self.session.modified = True

    def __iter__(self):
        from products.models import Product
        product_ids = self.cart.keys()
        products = Product.objects.filter(pk__in=product_ids)
        cart = self.cart.copy()

        for product in products:
            cart[str(product.pk)]['product'] = product

        for item in cart.values():
            item['price'] = float(item['price'])
            item['total'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(
            float(item['price']) * item['quantity']
            for item in self.cart.values()
        )

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()
