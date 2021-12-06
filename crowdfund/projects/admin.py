from django.contrib import admin
from .models import Project, Donation, Comment, Image, ReportComment, ReportProject, Rating,Reply

# Register your models here.
admin.site.register(Project)
admin.site.register(Donation)
admin.site.register(Image)
admin.site.register(Comment)
admin.site.register(ReportProject)
admin.site.register(ReportComment)
admin.site.register(Rating)
admin.site.register(Reply)