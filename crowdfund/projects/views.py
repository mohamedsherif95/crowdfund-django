from django.views.generic import CreateView, ListView, DetailView
from .models import Project
from .forms import AddProjectForm
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
        obj.save()
        form.save_m2m()
        return redirect('projects:home')


class ProjectList(ListView):

    model = Project
    paginate_by = 5

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