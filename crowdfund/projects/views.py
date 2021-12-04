
from django.db import models
from django.views.generic import CreateView, ListView, DetailView, DeleteView
from django.urls import reverse_lazy
from .models import Comment, Donation, Project, Image, Rating, Rating
from .forms import AddProjectForm, MakeDonationForm
from django.shortcuts import redirect, render
from django.db.models import Q, fields
from django.contrib import messages


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
        images = Image.objects.all().filter(project=project)
        rate = Rating.objects.filter(project=project)
        print(rate)
        total=0
        for r in rate:
            total = total+int(r.rate)
        if total == 0:
            avg = 0
        else:
            avg = total/len(rate)
        print(total)
        project_tags_ids = project.tags.values_list('id', flat=True)
        similar_projects = Project.objects.filter(tags__in=project_tags_ids).exclude(id=project.id).distinct()
        context["similar_projects"] = similar_projects
        context["images"] = images
        context['avg'] = avg
        return context


class ProjectCancel(DeleteView):
    model = Project
    template_name = 'projects/project_cancel.html'
    success_url = reverse_lazy('projects:home')



class RatingView(CreateView):
    model = Rating
    template_name = 'projects/rate.html'
    fields = ['rate']
   
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = Project.objects.get(pk=self.kwargs['pk'])
        context["project"] = project
        return context

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.project = Project.objects.get(pk=self.kwargs['pk'])
        obj.save()
        return redirect('projects:project_details',self.kwargs["pk"])
# class DeleteComment(DeleteView):
#     model = Comment
#     template_name = 'projects/delete_comment.html'

#     def get_success_url(self):
#         return reverse_lazy('accounts:profile', self.request.user.pk)

#     def get(self, *args, **kwargs):
#         return self.post(*args, **kwargs)


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
    fields = ['comment','rate']


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