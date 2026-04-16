"""URL routing for authentication API endpoints."""
from django.urls import path
from .views import RegisterView, LoginView, LogoutView, EmailCheckView

urlpatterns = [
    path('registration/', RegisterView.as_view(), name='registration'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('email-check/', EmailCheckView.as_view(), name='email-check'),
]