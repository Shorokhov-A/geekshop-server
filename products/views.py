from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView

from django.conf import settings
from django.core.cache import cache

from django.template.loader import render_to_string

from django.dispatch import receiver
from django.db.models.signals import pre_save, pre_delete
from django.db import connection

from products.models import ProductCategory, Product


# Create your views here.


class IndexTemplateView(TemplateView):
    template_name = 'products/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexTemplateView, self).get_context_data(**kwargs)
        context.update({
            'title': 'GeekShop',
            'header': 'GeekShop Store',
        })
        return context


class ProductsListView(ListView):
    model = Product
    paginate_by = 3
    template_name = 'products/products.html'
    context_object_name = 'products'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductsListView, self).get_context_data(**kwargs)
        context.update({
            'title': 'GeekShop - Каталог',
            'header': 'GeekShop',
            'categories': get_links_menu(),
        })
        return context

    def get_queryset(self):
        if self.kwargs.get('category'):
            category = get_category(self.kwargs['category'])
            return get_products_in_category_ordered_by_price(category.pk)
        return get_products()


def get_links_menu():
    if settings.LOW_CACHE:
        key = 'links_menu'
        links_menu = cache.get(key)
        if links_menu is None:
            links_menu = ProductCategory.objects.filter(is_active=True)
            cache.set(key, links_menu)
        return links_menu
    else:
        return ProductCategory.objects.filter(is_active=True)


def get_category(pk):
    if settings.LOW_CACHE:
        key = f'category_{pk}'
        category = cache.get(key)
        if category is None:
            category = get_object_or_404(ProductCategory, pk=pk)
            cache.set(key, category)
        return category
    else:
        return get_object_or_404(ProductCategory, pk=pk)


def get_products():
    if settings.LOW_CACHE:
        key = 'products'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(is_active=True, category__is_active=True).select_related('category')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(is_active=True, category__is_active=True).select_related('category')


def get_products_ordered_by_price():
    if settings.LOW_CACHE:
        key = 'products_ordered_by_price'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(is_active=True, category__is_active=True).order_by('price')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(is_active=True, category__is_active=True).order_by('price')


def get_products_in_category_ordered_by_price(pk):
    if settings.LOW_CACHE:
        key = f'products_in_category_ordered_by_price_{pk}'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(category__pk=pk, is_active=True,
                                              category__is_active=True).order_by('price')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(category__pk=pk, is_active=True, category__is_active=True).order_by('price')


def products_ajax(request, pk=None, page=1):
    if request.is_ajax():
        links_menu = get_links_menu()
        if pk:
            if pk == '0':
                category = {
                    'pk': 0,
                    'name': 'все'
                }
                products = get_products_ordered_by_price()
            else:
                category = get_category(pk)
                products = get_products_in_category_ordered_by_price(pk)

            paginator = Paginator(products, 3)
            try:
                products_paginator = paginator.page(page)
            except PageNotAnInteger:
                products_paginator = paginator.page(1)
            except EmptyPage:
                products_paginator = paginator.page(paginator.num_pages)

            content = {
                'links_menu': links_menu,
                'category': category,
                'products': products_paginator,
            }
            result = render_to_string(
                'products/includes/inc_products_list_content.html',
                context=content,
                request=request)
            return JsonResponse({'result': result})


@receiver(pre_save, sender=ProductCategory)
@receiver(pre_save, sender=Product)
@receiver(pre_delete, sender=ProductCategory)
@receiver(pre_delete, sender=Product)
def cache_clear(sender, **kwargs):
    if cache:
        cache.clear()


# def index(request):
#     context = {
#         'title': 'GeekShop',
#         'header': 'GeekShop Store',
#     }
#     return render(request, 'products/index.html', context)


# def products(request, category_id=None, page=1):
#     context = {
#         'title': 'GeekShop - Каталог',
#         'header': 'GeekShop',
#         'categories': ProductCategory.objects.all(),
#     }
#     if category_id:
#         products_list = Product.objects.filter(category_id=category_id)
#     else:
#         products_list = Product.objects.all()
#     paginator = Paginator(products_list, 3)
#     try:
#         products_paginator = paginator.page(page)
#     except PageNotAnInteger:
#         products_paginator = paginator.page(1)
#     except EmptyPage:
#         products_paginator = paginator.page(paginator.num_pages)
#     context['products'] = products_paginator
#     return render(request, 'products/products.html', context)
