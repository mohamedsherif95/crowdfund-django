from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    path('home/', views.index, name='home'),
    path('add_project/', views.AddProject.as_view(), name='add_project'),
    path('project_list/', views.ProjectList.as_view(), name='project_list'),
    path('project_details/<int:pk>/', views.ProjectDetails.as_view(), name='project_details'),
    path('project_details/<int:pk>/comment', views.LeaveComment.as_view(), name='project_comment'),
    path('project_details/<int:project_pk>/comment/<int:pk>', views.LeaveReply.as_view(), name='project_reply'),
    path('project_details/<int:pk>/cancel', views.ProjectCancel.as_view(), name='project_cancel'),
    path('project_details/<int:pk>/donate/', views.MakeDonation.as_view(), name='make_donation'),
    path('search_projects/', views.ProjectSearch.as_view(), name='search_projects'),
    # path('reports/', views.reports, name='reports'),
    path('report_project/<int:pk>', views.ReportProject.as_view(), name='report_project'),
    path('report_comment/<int:pk>', views.ReportComment.as_view(), name='report_comment'),
    path('project_rate/<int:pk>/', views.RatingView.as_view(), name='project_rate'),
    path('category_projects/<str:category>/', views.CategoryProjects.as_view(), name='category_projects'),
]