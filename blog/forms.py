from django import forms
from .models import Blog , Post , Categories

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['name' , 'logo' , 'bio' , 'lang' ,'email', 'template' , 'facebook' , 'instagram' , 'twitter' ,'linkedin','pinterest']

class PostForm(forms.ModelForm):
    def __init__(self,request , *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request
        blog_user = Blog.objects.get(user=self.request.user)
        self.fields['categorie'].queryset = Categories.objects.filter(blog=blog_user)
    class Meta:
        model = Post
        fields = ['title' ,'desc' ,'content' , 'categorie' , 'image' ]


class CategorieForm(forms.ModelForm):
    class Meta:
        model = Categories
        fields = [
            'name',
            'father',
            'is_father',
            'img', 
        ]
