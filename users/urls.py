from django.urls import path

from users.views import UserLoginView, RegistrationCreateView, ProfileUpdateView, UserLogoutView, verify

app_name = 'users'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('registration/', RegistrationCreateView.as_view(), name='registration'),
    path('profile/<int:pk>/', ProfileUpdateView.as_view(), name='profile'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('verify/<str:email>/<str:activation_key>', verify, name='verify'),
]
