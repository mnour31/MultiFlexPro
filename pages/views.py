from django.shortcuts import render 
from django.views import View

# Create your views here.

class Index(View):
    def get(self , request):

        context = {
            'name':'home',
        }
        return render(request, 'pages/index.html' , context)

class About(View):
    def get(self ,request):

        return render(request,'pages/about.html')