from django.views.generic import CreateView, ListView, DetailView, DeleteView
from django.urls import reverse_lazy
from .models import Comment, Donation, Project, Image, ReportProject, ReportComment
from .forms import AddProjectForm, MakeDonationForm
from django.shortcuts import redirect, render
from django.db.models import Q, Count
from django.contrib import messages
from datetime import datetime
from django.contrib.auth.decorators import login_required, permission_required


# Create your views here.
def index(request):
    # top_rated = Project.objects.order_by('-rating')[:5]
    top_featured = Project.objects.filter(is_featured=True).order_by('-start_time')[:5]
    top_latest = Project.objects.order_by('-start_time')[:5]

    context = {
        'top_latest': top_latest,
        # 'top_rated': top_rated,
        'top_featured': top_featured,
    }
    print(context['top_featured'])
    print(context['top_featured'][0].category)
    print(context['top_featured'][1].category)
    return render(request, 'projects/home.html', context)


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


class ProjectCancel(DeleteView):
    model = Project
    template_name = 'projects/project_cancel.html'
    success_url = reverse_lazy('projects:home')


class MakeDonation(CreateView):
    model = Donation
    form_class = MakeDonationForm
    template_name = 'projects/make_donation.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = Project.objects.get(pk=self.kwargs['pk'])
        context["project"] = project
        return context

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        project = Project.objects.get(pk=self.kwargs['pk'])
        new_current = project.current + obj.amount
        if new_current > project.total_target:
            messages.error(self.request, 'the amount donated would exceed the fund target. Please recalculate.')
            return redirect('projects:make_donation', self.kwargs['pk'])
        obj.project = project
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


# @permission_required('projects.view_report', raise_exception=True)
# def reports(request):
#     projects_reports = Project.objects.annotate(times_reported=Count('report')).filter(times_reported__gt=0).all()

#     context = {
#                'projects_reports' : projects_reports,
#                }
#     return render(request, 'projects/reports.html', context)

