from django.contrib import admin
from .models import Project, Donation, Comment, Image

# Register your models here.
admin.site.register(Project)
admin.site.register(Donation)
admin.site.register(Image)
admin.site.register(Comment)
