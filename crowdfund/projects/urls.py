from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    path('home/', views.index, name='home')
]