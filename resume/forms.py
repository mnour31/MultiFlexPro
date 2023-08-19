from django import forms
from .models import Cv , Skille , Experience , Service , Portfolio , Testimonial ,JobTitle

class CvForm(forms.ModelForm):
    class Meta:
        model = Cv
        fields = '__all__'
        exclude = ['user', 'created_date' , 'slug' ]

class JobTitleForm(forms.ModelForm):
    class Meta:
        model = JobTitle
        fields = ['name']

class SkilleForm(forms.ModelForm):
    class Meta:
        model = Skille
        fields = ['name' , 'progrise']

class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = ['name' , 'company_name' , 'desc' , 'date_from' , 'date_to']

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name' , 'desc' ,'image']

class PortfolioForm(forms.ModelForm):
    class Meta:
        model = Portfolio
        fields = ['name' ,'image']

class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ['client_name' ,'what_he_say' ,'image']