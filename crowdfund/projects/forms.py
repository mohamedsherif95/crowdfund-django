from typing import ValuesView
from django import forms 
from .models import Project, Donation, ReportComment, ReportProject
from django.forms.widgets import NumberInput
from django.forms.models import inlineformset_factory

class AddProjectForm(forms.ModelForm):
    
    start_time = forms.DateField(label="Start Date", required=True,
     widget=NumberInput(attrs={'type':'date'}))

    end_time = forms.DateField(label="End Date", required=True,
     widget=NumberInput(attrs={'type':'date'}))

    class Meta:
        model = Project
        fields = '__all__'
        exclude = ('user',)


class MakeDonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ['amount']


class MakeReportForm(forms.ModelForm):
    class Meta:
        models = (ReportProject, ReportComment)
        fields = ['category', 'report_message']
        
# class ImageForm(forms.ModelForm):

#     image = forms.ImageField(label='Images')
#     class Meta:
#         model = Images
#         fields = ('image', )
