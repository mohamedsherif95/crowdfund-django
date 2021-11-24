from django.http import HttpResponse
from django.views.generic import CreateView, ListView, DetailView
from .models import Project
from .forms import AddProjectForm
from django.urls import reverse_lazy
from django.shortcuts import redirect


# Create your views here.
def index(request):
    return HttpResponse("<h1>Home Page</h1>")


class AddProject(CreateView):
    model = Project
    form_class = AddProjectForm
    template_name = 'projects/add_project.html'
    # success_url = reverse_lazy('projects:home')

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        form.save_m2m()
        return redirect('projects:home')


class ProjectList(ListView):

    model = Project
    paginate_by = 5


class ProjectDetails(DetailView):

    model = Project