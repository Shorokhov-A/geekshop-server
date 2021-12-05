from django.urls import path

from admins.views import IndexTemplateView, UserCreateView, UserListView, UserUpdateView, UserDeleteView, \
    CategoryListView, ProductListView

app_name = 'baskets'

urlpatterns = [
    path('', IndexTemplateView.as_view(), name='index'),
    path('users/', UserListView.as_view(), name='admin_users'),
    path('users-create/', UserCreateView.as_view(), name='admin_users_create'),
    path('users-update/<int:pk>/', UserUpdateView.as_view(), name='admin_users_update'),
    path('users-delete/<int:pk>/', UserDeleteView.as_view(), name='admin_users_delete'),
    path('categories/', CategoryListView.as_view(), name='admin_categories'),
    path('products/', ProductListView.as_view(), name='admin_products'),
]
