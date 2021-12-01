from django import forms 
from .models import Project, Donation
from django.forms.widgets import NumberInput

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


# class ImageForm(forms.ModelForm):

#     image = forms.ImageField(label='Images')
#     class Meta:
#         model = Images
#         fields = ('image', )
