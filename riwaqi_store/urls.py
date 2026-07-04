from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from products.views import home
from core.views import dashboard

# Customize Admin Site
admin.site.site_header = '🕌 رواق المسلم - لوحة التحكم'
admin.site.site_title = 'رواق المسلم'
admin.site.index_title = 'إدارة المتجر'

urlpatterns = [
    path('admin/dashboard/', dashboard, name='admin_dashboard'),
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('', include('products.urls')),
    path('', include('orders.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
