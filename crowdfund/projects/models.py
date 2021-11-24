from django.db import models
from taggit.managers import TaggableManager
from accounts.models import User

# Create your models here.
class Project(models.Model):
    title = models.CharField(max_length=250)
    details = models.TextField()
    CATEGORY_CHOICES = [
        ('SC', 'Social'),
        ('PO', 'Political'),
        ('SP', 'Sports'),
        ('ED', 'Educational'),
    ]
    category = models.CharField(
        max_length=2,
        choices=CATEGORY_CHOICES,
        default='SC',
    )
    images = models.ImageField(null=False, blank=False)
    total_target = models.IntegerField()
    tags = TaggableManager()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    def __str__(self):
        return self.title


# class Images(models.Model):
#     post = models.ForeignKey(Project, default=None, on_delete=models.CASCADE, blank=True, null=True)
#     image = models.ImageField(upload_to='images/', blank=True, null=True)


# class Deonate(models.Model):
    
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     project = models.ForeignKey(Project, on_delete=models.CASCADE)
    
    