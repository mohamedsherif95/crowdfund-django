from django.urls import path
from . import views , api
from knox import views as knox_views
from django.views.generic.base import TemplateView



app_name = 'accounts'

urlpatterns = [
    path('', views.landing, name='landing'),
    path('register/', views.RegisterationView.as_view(), name='register'),
    path('activate/<uidb64>/<token>/', views.VerificationView.as_view(), name='activate'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('not-verified/', TemplateView.as_view(template_name='accounts/not_verified.html'), name='not_verified'),
    path('password_reset/', views.password_reset_request, name='password_reset'),
    path('profile/', views.profile, name='profile_page'),
    path('profile/<int:pk>/', views.ProfileView.as_view(), name='profile'),
    path('profile/<int:pk>/update', views.ProfileUpdateView.as_view(), name='profile_update'),
    path('profile/<int:pk>/delete', views.ProfileDeleteView.as_view(), name='profile_delete'),
    path('profile/<int:pk>/projects', views.UserProjects.as_view(), name='user_projects'),
    path('profile/<int:pk>/donations', views.UserDonations.as_view(), name='user_donations'),
    
    
    #APIs
    
    path('api/register/', api.RegisterAPI.as_view(), name='registerapi'),
    path('api/login/', api.LoginAPI.as_view(), name='loginapi'),
    path('api/logout/', knox_views.LogoutView.as_view(), name='logoutapi'),
    path('api/user/', api.UserAPI.as_view()),
    # path('api/logoutall/', knox_views.LogoutAllView.as_view(), name='logoutallapi'),

]

