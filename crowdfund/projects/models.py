from django.db import models
from taggit.managers import TaggableManager
from accounts.models import User
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Project(models.Model):
    title = models.CharField(max_length=250)
    details = models.TextField()
    CATEGORY_CHOICES = [
        ('Social', 'Social'),
        ('Political', 'Political'),
        ('Sports', 'Sports'),
        ('Educational', 'Educational'),
    ]
    category = models.CharField(
        max_length=11,
        choices=CATEGORY_CHOICES,
        default='Social',
    )
    images = models.ImageField(_('Project Cover'),null=False, blank=False)
    total_target = models.PositiveIntegerField()
    current = models.PositiveIntegerField(default=0)
    tags = TaggableManager()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    avg_rate = models.FloatField(default=0)

    def __str__(self):
        return self.title

    def get_details(self):
        return self.details[:25]

    def can_cancel(self):
        return self.current < (self.total_target * 0.25)

    def target_reached(self):
        return self.current == self.total_target

    def calc_avg_rate(self):
        ratings = Rating.objects.filter(project=self)
        total=0
        for rating in ratings:
            total = total+int(rating.rate)
        if total == 0:
            avg = 0
        else:
            avg = total/ratings.count()
        if avg % 1 == 0:
            self.avg_rate = int(avg)
            return int(avg)
        self.avg_rate = round(avg, 1)
        return round(avg, 1)

    
class Image(models.Model):
    project = models.ForeignKey(Project, default=None, on_delete=models.CASCADE, blank=True, null=True)
    image = models.ImageField( blank=True, null=True)

    def __str__(self):
        return f"id: {self.id}, Project: {self.project}"


class Donation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.amount} from {self.user.username} to {self.project.title}"

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    CATEGORY_CHOICES = [
        ('1', 1),
        ('2', 2),
        ('3', 3),
        ('4', 4),
        ('5', 5),
    ]
    rate = models.CharField(
        max_length=2,
        choices=CATEGORY_CHOICES,
        default='1',
    )

    def __str__(self):
        return f"{self.user.username} gave {self.project} {self.rate}/5"

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    comment = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"user: {self.user.username}, project: {self.project.title}"

    
class ReportProject(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    REPORT_CHOICES = [
        ('hm', 'Harmful'),
        ('fk', 'Fake'),
        ('il', 'Illegale'),
        ('ab', 'Abuse'),
    ]
    category = models.CharField(
        max_length=2,
        choices=REPORT_CHOICES,
        default='fk',
    )
    report_message = models.TextField()    
    
    def __str__(self):
        return f"Report from user: {self.user.username},on project: {self.project.title}"
    
    
class ReportComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    REPORT_CHOICES = [
        ('hm', 'Harmful'),
        ('fk', 'Fake'),
        ('il', 'Illegale'),
        ('ab', 'Abuse'),
    ]
    category = models.CharField(
        max_length=2,
        choices=REPORT_CHOICES,
        default='fk',
    )
    report_message = models.TextField()
    
    def __str__(self):
        return f"Report from user: {self.user.username},on comment: {self.comment}"    