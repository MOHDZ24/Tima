from django.contrib import admin
from .models import Category, Product, ProductImage


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'is_active', 'order', 'created_at']
    list_filter = ['is_active', 'parent']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_active', 'order']


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'category', 'price', 'old_price',
        'is_new', 'is_on_sale', 'is_active', 'stock', 'views_count'
    ]
    list_filter = ['is_active', 'is_new', 'is_on_sale', 'category']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['price', 'old_price', 'is_new', 'is_on_sale', 'is_active', 'stock']
    inlines = [ProductImageInline]
    fieldsets = (
        ('معلومات أساسية', {
            'fields': ('name', 'slug', 'category', 'description')
        }),
        ('الأسعار', {
            'fields': ('price', 'old_price')
        }),
        ('الصور', {
            'fields': ('image', 'image_2', 'image_3')
        }),
        ('الحالة', {
            'fields': ('is_new', 'is_on_sale', 'is_active', 'stock', 'order')
        }),
    )


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
