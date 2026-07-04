from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product_name', 'product_image', 'price', 'quantity']

    def has_add_permission(self, request, obj=None):
        return False


class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'pk', 'full_name', 'phone', 'wilaya',
        'status', 'payment_method', 'total', 'created_at'
    ]
    list_filter = ['status', 'payment_method', 'wilaya', 'created_at']
    search_fields = ['full_name', 'phone', 'wilaya', 'commune']
    list_editable = ['status']
    readonly_fields = [
        'full_name', 'phone', 'phone2', 'wilaya', 'commune',
        'address', 'notes', 'payment_method', 'subtotal',
        'shipping_cost', 'total', 'created_at', 'updated_at'
    ]
    inlines = [OrderItemInline]
    fieldsets = (
        ('معلومات العميل', {
            'fields': ('full_name', 'phone', 'phone2', 'wilaya', 'commune', 'address')
        }),
        ('معلومات الطلب', {
            'fields': ('status', 'payment_method', 'tracking_number', 'notes')
        }),
        ('المبالغ', {
            'fields': ('subtotal', 'shipping_cost', 'total')
        }),
        ('التواريخ', {
            'fields': ('created_at', 'updated_at')
        }),
    )

    def has_add_permission(self, request):
        return False


admin.site.register(Order, OrderAdmin)
