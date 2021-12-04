from django.views.generic import CreateView, ListView, DetailView
from .models import Comment, Donation, Project, Image, ReportProject, ReportComment
from .forms import AddProjectForm, MakeDonationForm, MakeReportForm
from django.shortcuts import redirect, render
from django.db.models import Q
from django.db.models import Count
from datetime import datetime
from django.contrib.auth.decorators import login_required, permission_required


# Create your views here.
def index(request):
    return render(request, 'projects/home.html')


class AddProject(CreateView):
    model = Project
    form_class = AddProjectForm
    template_name = 'projects/add_project.html'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        images = self.request.FILES.getlist('images')
        obj.save()
        form.save_m2m()
        for image in images:
            photo = Image.objects.create(project=obj,image=image)
        return redirect('projects:home')


class ProjectList(ListView):

    model = Project
    # paginate_by = 100

class ProjectSearch(ListView):

    model = Project

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        queryset = self.model.objects.all()
        if query:
            queryset = self.model.objects.filter(Q(title__icontains=query) | Q(details__icontains=query))
        return queryset


class ProjectDetails(DetailView):

    model = Project

    def get_similar_projects(self):
        project_tags_ids = self.tags.values_list('id', flat=True)
        print('excuted')
        print(project_tags_ids)
        return project_tags_ids

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = Project.objects.get(pk=self.kwargs['pk'])
        project_tags_ids = project.tags.values_list('id', flat=True)
        similar_projects = Project.objects.filter(tags__in=project_tags_ids).exclude(id=project.id).distinct()
        context["similar_projects"] = similar_projects
        return context


class MakeDonation(CreateView):
    model = Donation
    form_class = MakeDonationForm
    template_name = 'projects/make_donation.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project_pk = self.kwargs['pk']
        context["project_pk"] = project_pk
        return context

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.project = Project.objects.get(pk=self.kwargs['pk'])
        obj.save()
        return redirect('projects:project_details', self.kwargs['pk'])


class LeaveComment(CreateView):
    model = Comment
    template_name = 'projects/project_comment.html'
    fields = ['comment']


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project_pk = self.kwargs['pk']
        context["project_pk"] = project_pk
        return context

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.project = Project.objects.get(pk=self.kwargs['pk'])
        obj.save()
        return redirect('projects:project_details', self.kwargs['pk'])
    
# You will allow users to report projects and comments made by other users, 
# and you will then let moderators choose to block a user completely and/or hide their projects or comments.
# To get started with this, create a moderator group in the admin dashboard. 
# The moderator group will be given access to change both projects and users and the ability to view reports.



class ReportProject(CreateView): 
    model = ReportProject
    template_name = 'projects/project_report_form.html'
    fields = ['category', 'report_message']  
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project_pk = self.kwargs['pk']
        context["project_pk"] = project_pk
        return context
    
    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.project = Project.objects.get(pk=self.kwargs['pk'])
        obj.save()
        return redirect('projects:project_details', self.kwargs['pk'])
 
class ReportComment(CreateView): 
    model = ReportComment
    template_name = 'projects/comment_report_form.html'
    fields = ['category', 'report_message']  
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comment = Comment.objects.get(pk=self.kwargs['pk'])
        context["comment"] = comment
        return context
    
    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.comment = Comment.objects.get(pk=self.kwargs['pk'])
        obj.save()
        return redirect('projects:home')
    
# def reports(request):
#     url_report = request.get_full_path()
#     if request.method == 'POST':
#         form = MakeReportForm(request.POST or None)
#         if form.is_valid():
#             new_form = form.save(commit=False)
#             new_form.reporting_url = url_report
#             new_form.save()    

@permission_required('projects.view_report', raise_exception=True)
def reports(request):
    projects_reports = Project.objects.annotate(times_reported=Count('report')).filter(times_reported__gt=0).all()
    # comments_reports = Comment.objects.annotate(times_reported=Count('report')).filter(times_reported__gt=0).all()
    context = {
               'projects_reports' : projects_reports,
            #    'comments_reports' : comments_reports
               }
    return render(request, 'projects/reports.html', context)


# def report_project(request, project_id):
#     project = Project.objects.get(id=project_id)
#     # report, created = Report.objects.get_or_create(reported_by=request.user, project=project)
#     if request.method == 'POST':
#         form = MakeReportForm(request.POST or None)
#         if form.is_valid():
#             new_form = form.save(commit=False)
#             new_form.project = request.user
#             new_form.save()  
#             return redirect('projects:project_details', id=project_id)  
#     else:
#         form = MakeReportForm()
#     # if created:
#     #     report.save()
#     return render(request, 'projects/project_report_form.html', {'form' : form})
    

# def report_comment(request, comment_id):
#     comment = Comment.objects.get(id=comment_id)
#     report, created = Report.objects.get_or_create(reported_by=request.user, comment=comment)
#     if created:
#         report.save()
#     return redirect('projects:project_details', id=comment_id)




# @permission_required('feedapp.change_user')
# def block_user(request, user_id):
#     User = get_user_model()

#     user = User.objects.get(id=user_id)
#     for post in user.post_set.all():
#         if not post.hidden:
#             post.hidden = True
#             post.hidden_by = request.user
#             post.date_hidden = datetime.now()
#             post.save()

#     user.is_active = False
#     user.save()

#     return redirect('reports')