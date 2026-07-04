from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Product, Category


def product_list(request):
    products = Product.objects.filter(is_active=True)
    categories = Category.objects.filter(parent__isnull=True, is_active=True)
    query = request.GET.get('q', '')
    category_slug = request.GET.get('category', '')

    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )

    if category_slug:
        category = Category.objects.filter(slug=category_slug).first()
        if category:
            # Include subcategory products too
            sub_ids = category.children.values_list('pk', flat=True)
            products = products.filter(
                Q(category=category) | Q(category__in=sub_ids)
            )

    context = {
        'products': products,
        'categories': categories,
        'query': query,
        'selected_category': category_slug,
    }
    return render(request, 'products/product_list.html', context)


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk, is_active=True)
    # Increment views
    Product.objects.filter(pk=pk).update(views_count=product.views_count + 1)
    # Related products
    related = Product.objects.filter(
        category=product.category, is_active=True
    ).exclude(pk=pk)[:6]
    context = {
        'product': product,
        'related_products': related,
    }
    return render(request, 'products/product_detail.html', context)


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug, is_active=True)
    sub_ids = category.children.values_list('pk', flat=True)
    products = Product.objects.filter(
        Q(category=category) | Q(category__in=sub_ids),
        is_active=True
    )
    categories = Category.objects.filter(parent__isnull=True, is_active=True)
    context = {
        'category': category,
        'products': products,
        'categories': categories,
    }
    return render(request, 'products/category_detail.html', context)


def home(request):
    special_offers = Product.objects.filter(
        is_active=True, is_on_sale=True
    )[:10]
    new_products = Product.objects.filter(
        is_active=True, is_new=True
    )[:10]
    all_products = Product.objects.filter(is_active=True)[:20]
    categories = Category.objects.filter(parent__isnull=True, is_active=True)

    context = {
        'special_offers': special_offers,
        'new_products': new_products,
        'all_products': all_products,
        'categories': categories,
    }
    return render(request, 'core/home.html', context)
