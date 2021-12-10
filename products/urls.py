from django.urls import path
from django.views.decorators.cache import cache_page

from products.views import ProductsListView, products_ajax

app_name = 'products'

urlpatterns = [
    path('', ProductsListView.as_view(), name='index'),
    path('<int:category>/', ProductsListView.as_view(), name='category'),
    path('<int:category>/ajax/', cache_page(3600)(products_ajax)),
    path('<int:category>/page/<int:page>/', ProductsListView.as_view(), name='page'),
    path('<int:category>/page/<int:page>/ajax/', cache_page(3600)(products_ajax)),
    path('page/<int:page>/', ProductsListView.as_view(), name='page_all'),
    path('page/<int:page>/ajax/', cache_page(3600)(products_ajax)),
]
