from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    path('home/', views.index, name='home'),
    path('add_project/', views.AddProject.as_view(), name='add_project'),
    path('project_list/', views.ProjectList.as_view(), name='project_list'),
    path('project_details/<int:pk>/', views.ProjectDetails.as_view(), name='project_details'),
    path('project_details/<int:pk>/comment', views.LeaveComment.as_view(), name='project_comment'),
    path('project_details/<int:pk>/donate/', views.MakeDonation.as_view(), name='make_donation'),
    path('search_projects/', views.ProjectSearch.as_view(), name='search_projects'),
]