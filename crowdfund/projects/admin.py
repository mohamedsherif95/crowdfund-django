from django.contrib import admin
from .models import Image, Project, Donation

# Register your models here.
admin.site.register(Project)
admin.site.register(Donation)
admin.site.register(Image)