from django.urls import path
from django.views.generic.base import TemplateView
from . import views


app_name = 'accounts'

urlpatterns = [
    path('', views.landing, name='landing'),
    path('register/', views.RegisterationView.as_view(), name='register'),
    path('activate/<uidb64>/<token>', views.VerificationView.as_view(), name='activate'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('not-verified/', TemplateView.as_view(template_name='accounts/not_verified.html'), name='not_verified'),
]

