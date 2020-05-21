from django.shortcuts import render, get_object_or_404
from .models import Product, Category, Brand, Shop


def index(request):
    return render(request, 'base.html')


def product_list(request, slug):
    category = get_object_or_404(Category, slug=slug)
    categories = category.get_descendants().order_by('tree_id', 'id', 'name')

    products = Product.objects.filter(category__in=category.get_descendants(include_self=True))

    context = {'products': products}

    return render(request, 'product/product_list.html', context)