from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView

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
            'categories': ProductCategory.objects.all(),
        })
        return context

    def get_queryset(self):
        if self.kwargs.get('category'):
            category = get_object_or_404(ProductCategory, id=self.kwargs['category'])
            return Product.objects.filter(category=category).select_related()
        return Product.objects.all()


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
