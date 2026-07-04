from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import timedelta
from products.models import Product, Category
from orders.models import Order, OrderItem


@staff_member_required
def dashboard(request):
    """لوحة التحكم الاحترافية مع الإحصائيات والتقارير"""
    today = timezone.now().date()
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)

    # إحصائيات عامة
    total_orders = Order.objects.count()
    total_products = Product.objects.filter(is_active=True).count()
    total_revenue = Order.objects.filter(status='delivered').aggregate(total=Sum('total'))['total'] or 0
    total_customers = Order.objects.values('phone').distinct().count()

    # إحصائيات اليوم
    today_orders = Order.objects.filter(created_at__date=today).count()
    today_revenue = Order.objects.filter(created_at__date=today).aggregate(total=Sum('total'))['total'] or 0

    # إحصائيات الأسبوع
    week_orders = Order.objects.filter(created_at__date__gte=week_ago).count()
    week_revenue = Order.objects.filter(created_at__date__gte=week_ago).aggregate(total=Sum('total'))['total'] or 0

    # إحصائيات الشهر
    month_orders = Order.objects.filter(created_at__date__gte=month_ago).count()
    month_revenue = Order.objects.filter(created_at__date__gte=month_ago).aggregate(total=Sum('total'))['total'] or 0

    # الطلبات حسب الحالة
    orders_by_status = {
        'pending': Order.objects.filter(status='pending').count(),
        'confirmed': Order.objects.filter(status='confirmed').count(),
        'shipped': Order.objects.filter(status='shipped').count(),
        'delivered': Order.objects.filter(status='delivered').count(),
        'cancelled': Order.objects.filter(status='cancelled').count(),
    }

    # آخر 10 طلبات
    recent_orders = Order.objects.all()[:10]

    # المنتجات الأكثر مبيعاً
    top_products = (
        OrderItem.objects
        .values('product_name')
        .annotate(total_sold=Sum('quantity'), total_revenue=Sum('price'))
        .order_by('-total_sold')[:10]
    )

    # المنتجات الأكثر مشاهدة
    most_viewed = Product.objects.filter(is_active=True).order_by('-views_count')[:10]

    # المنتجات منخفضة المخزون
    low_stock = Product.objects.filter(is_active=True, stock__lte=5).order_by('stock')[:10]

    # إحصائيات المبيعات آخر 7 أيام
    daily_sales = []
    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        day_orders = Order.objects.filter(created_at__date=day)
        daily_sales.append({
            'date': day.strftime('%Y-%m-%d'),
            'label': day.strftime('%a'),
            'orders': day_orders.count(),
            'revenue': float(day_orders.aggregate(total=Sum('total'))['total'] or 0),
        })

    # إحصائيات حسب الولاية
    orders_by_wilaya = (
        Order.objects
        .values('wilaya')
        .annotate(count=Count('id'), revenue=Sum('total'))
        .order_by('-count')[:10]
    )

    # إحصائيات طرق الدفع
    payment_stats = (
        Order.objects
        .values('payment_method')
        .annotate(count=Count('id'))
        .order_by('-count')
    )

    # إحصائيات الفئات
    category_stats = []
    for cat in Category.objects.filter(parent__isnull=True):
        product_count = Product.objects.filter(
            Q(category=cat) | Q(category__parent=cat),
            is_active=True
        ).count()
        category_stats.append({
            'name': cat.name,
            'count': product_count,
        })

    context = {
        'title': 'لوحة التحكم',
        # عام
        'total_orders': total_orders,
        'total_products': total_products,
        'total_revenue': total_revenue,
        'total_customers': total_customers,
        # اليوم
        'today_orders': today_orders,
        'today_revenue': today_revenue,
        # الأسبوع
        'week_orders': week_orders,
        'week_revenue': week_revenue,
        # الشهر
        'month_orders': month_orders,
        'month_revenue': month_revenue,
        # تفصيلي
        'orders_by_status': orders_by_status,
        'recent_orders': recent_orders,
        'top_products': top_products,
        'most_viewed': most_viewed,
        'low_stock': low_stock,
        'daily_sales': daily_sales,
        'orders_by_wilaya': orders_by_wilaya,
        'payment_stats': payment_stats,
        'category_stats': category_stats,
    }
    return render(request, 'admin/dashboard.html', context)
