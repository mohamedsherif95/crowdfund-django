from django.contrib import admin
from .models import Project, Donation, Comment

# Register your models here.
admin.site.register(Project)
admin.site.register(Donation)
admin.site.register(Comment)