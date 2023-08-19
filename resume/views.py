from django.shortcuts import render , redirect
from django.views import View
from .forms import CvForm , JobTitleForm , SkilleForm , ExperienceForm , ServiceForm ,  PortfolioForm , TestimonialForm
from .models import Cv , JobTitle , Skille , Experience , Service , Portfolio , Testimonial
from django.contrib import messages
from django.core.mail import send_mail
# Create your views here.

def mysend_mail(request):
    if request.method == 'POST':
        cv_id = request.POST.get('cv-id')
        cv = Cv.objects.get(id=cv_id)
        recipient_list =[ cv.email]
        subject = request.POST.get('subject')
        name = request.POST.get('name')
        message = request.POST.get('message')
        email_from = request.POST.get('email')

        subject = f'from email : {email_from} name:{name}'
        send_mail(subject,message,email_from,recipient_list)
        return redirect(f'/cv/{cv.slug}/{cv.id}')

class CreateCv(View):
    def get(self, request):
        try:
            user_cv = Cv.objects.get(user=request.user)
            if user_cv != None:
                return redirect('cv_manage')
        except:
            pass
        form = CvForm()
        context = {
            'form':form,
        }
        return render(request,'cv/create_cv.html' , context)
    def post(self,request):
        form = CvForm(request.POST,request.FILES)
        if form.is_valid():
            myform = form.save(commit=False)
            myform.user = request.user
            myform.save()
            return redirect('cv_manage')

class CvManage(View):
    def get(self,request):
        cv = Cv.objects.get(user=request.user)
        cv_form = CvForm(instance=cv)
        jobtitleform = JobTitleForm()
        skilleform = SkilleForm()
        experienceform = ExperienceForm()
        serviceform = ServiceForm()
        portfolioform = PortfolioForm()
        testimonialform = TestimonialForm()
        context = {
            'cv':cv,
            'cv_form':cv_form,
            'jobtitleform':jobtitleform,
            'skilleform':skilleform,
            'experienceform':experienceform,
            'serviceform':serviceform,
            'portfolioform':portfolioform,
            'testimonialform':testimonialform,
        }
        return render(request,'cv/cv_manage.html' , context)
    def post(self,request):
        cv = Cv.objects.get(user=request.user)
        cv_form = CvForm(request.POST , request.FILES , instance=cv)
        if cv_form.is_valid():
            myform = cv_form.save(commit=False)
            myform.user = request.user
            myform.save()
            return redirect('cv_manage')

def job_title(request):
    if request.method == "POST":
        if 'delete-job' in request.POST:
            job = JobTitle.objects.get(id=request.POST['delete-job'])
            job.delete()
            return redirect('cv_manage')
        form = JobTitleForm(request.POST)
        if form.is_valid():
            cv = Cv.objects.get(user=request.user)
            myform = form.save(commit=False)
            myform.cv = cv
            myform.save()
            return redirect('cv_manage')

def skilles(request): 
    if request.method == "POST":
        if 'delete-skill' in request.POST:
            skill = Skille.objects.get(id=request.POST['delete-skill'])
            skill.delete()
            messages.info(request, f" Has been deleted {skill.name} ")
            return redirect('cv_manage')
        form = SkilleForm(request.POST)
        if form.is_valid():
            cv = Cv.objects.get(user=request.user)
            myform = form.save(commit=False)
            myform.cv = cv 
            myform.save()
            messages.info(request, f" Has been created {myform.name} ")
            return redirect('cv_manage')

def experience(request):
    if request.method == 'POST':
        if 'delete-experience' in request.POST:
            experience = Experience.objects.get(id=request.POST['delete-experience'])
            experience.delete()
            messages.info(request, f" Has been deleted {experience.name} ")
            return redirect('cv_manage')
        form = ExperienceForm(request.POST)
        if form.is_valid():
            cv = Cv.objects.get(user=request.user)
            myform = form.save(commit=False)
            myform.cv = cv 
            myform.save()
            messages.info(request, f" Has been created {myform.name} ")
            return redirect('cv_manage')

def services(request): 
    if request.method == "POST":
        if 'delete-service' in request.POST:
            service = Service.objects.get(id=request.POST['delete-service'])
            service.delete()
            messages.info(request, f" Has been deleted {service.name} ")
            return redirect('cv_manage')
        form = ServiceForm(request.POST , request.FILES)
        if form.is_valid():
            cv = Cv.objects.get(user=request.user)
            myform = form.save(commit=False)
            myform.cv = cv 
            myform.save()
            messages.info(request, f" Has been created {myform.name} ")
            return redirect('cv_manage')

def portfolio(request): 
    if request.method == "POST":
        if 'delete-portfolio' in request.POST:
            portfolio = Portfolio.objects.get(id=request.POST['delete-portfolio'])
            portfolio.delete()
            messages.info(request, f" Has been deleted {portfolio.name} ")
            return redirect('cv_manage')
        form = PortfolioForm(request.POST , request.FILES)
        if form.is_valid():
            cv = Cv.objects.get(user=request.user)
            myform = form.save(commit=False)
            myform.cv = cv 
            myform.save()
            messages.info(request, f" Has been created {myform.name} ")
            return redirect('cv_manage')

def testimonial(request): 
    if request.method == "POST":
        if 'delete-testimonial' in request.POST:
            testimonial = Testimonial.objects.get(id=request.POST['delete-testimonial'])
            testimonial.delete()
            messages.info(request, f" Has been deleted {testimonial.client_name} ")
            return redirect('cv_manage')
        form = TestimonialForm(request.POST , request.FILES)
        if form.is_valid():
            cv = Cv.objects.get(user=request.user)
            myform = form.save(commit=False)
            myform.cv = cv 
            myform.save()
            messages.info(request, f" Has been created {myform.client_name} ")
            return redirect('cv_manage')

class ViewCv(View):
    def get(self,request ,slug,id):
        cv = Cv.objects.get(id=id)
        
        context = {
            'cv':cv,
        }
        return render(request , 'cv/nour/index.html' ,context)