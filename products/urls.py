from django.urls import path

from products.views import ProductsListView

app_name = 'products'

urlpatterns = [
    path('', ProductsListView.as_view(), name='index'),
    path('<int:category>/', ProductsListView.as_view(), name='category'),
    path('<int:category>/page/<int:page>/', ProductsListView.as_view(), name='page'),
    path('page/<int:page>/', ProductsListView.as_view(), name='page_all'),
]
