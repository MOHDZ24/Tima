from django.contrib import admin
from django.utils.html import format_html
from .models import SiteSettings, DeliveryPrice, SliderImage


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('🏪 معلومات المتجر', {
            'fields': ('store_name', 'store_subtitle', 'logo', 'favicon')
        }),
        ('🎨 الألوان', {
            'fields': ('primary_color', 'secondary_color', 'accent_color'),
            'description': 'غيّر الألوان لتحديث مظهر الموقع فوراً'
        }),
        ('📱 التواصل الاجتماعي', {
            'fields': ('phone', 'email', 'address', 'instagram', 'tiktok', 'facebook', 'whatsapp')
        }),
        ('🖼️ الرئيسية', {
            'fields': ('hero_title', 'hero_subtitle', 'hero_button_text')
        }),
        ('🚚 الشحن', {
            'fields': ('free_shipping_min', 'default_shipping_cost')
        }),
        ('⚙️ إعدادات أخرى', {
            'fields': ('footer_text', 'maintenance_mode', 'show_special_offers',
                       'show_new_products', 'products_per_page', 'whatsapp_float')
        }),
    )

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(DeliveryPrice)
class DeliveryPriceAdmin(admin.ModelAdmin):
    list_display = ['wilaya', 'price', 'estimated_days', 'is_active']
    list_filter = ['is_active']
    search_fields = ['wilaya']
    list_editable = ['price', 'estimated_days', 'is_active']


@admin.register(SliderImage)
class SliderImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'order', 'image_preview']
    list_filter = ['is_active']
    list_editable = ['is_active', 'order']

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="50" style="object-fit:cover;border-radius:5px;">', obj.image.url)
        return '-'
    image_preview.short_description = 'معاينة'
