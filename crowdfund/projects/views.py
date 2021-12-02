from django.views.generic import CreateView, ListView, DetailView
from .models import Comment, Donation, Project, Image
from .forms import AddProjectForm, MakeDonationForm
from django.shortcuts import redirect, render
from django.db.models import Q


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