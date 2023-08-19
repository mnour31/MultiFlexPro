from django import forms
from .models import Slider , Brand

class SliderForm(forms.ModelForm):
    class Meta:
        model = Slider
        fields = ['name','image','url']

class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ['name','image']