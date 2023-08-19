from django.shortcuts import render , redirect
from django.views.generic import CreateView
from django.views import View
from django.contrib.auth import login, authenticate , logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm 
from .forms import UserForm
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView 
from .models import Profile
from .forms import UserFormProfile , ProfileForm
from resume.models import Cv
from shop.models import Shop
# Create your views here.

class Register(CreateView):
    template_name = 'register/register.html'
    form_class = UserForm
    success_url = reverse_lazy('index')

def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect("index")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="register/login.html", context={"form":form})

def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect("index")


class ProfileView(DetailView):
	model = Profile
	template_name = 'profile/profile.html'

	def get_context_data(self,**kwargs):
		context = super().get_context_data(**kwargs)
		user_profile=kwargs['object']
		try:
			cv = Cv.objects.get(user=user_profile.user)
			context['cv'] = cv
		except:
			cv = None
			context['cv'] = cv

		try:
			shop = Shop.objects.get(user=user_profile.user)
			context['shop'] = shop
		except:
			shop = None
			context['shop'] = shop

		return context

class ProfileEdit(View):
	def post(self, request):
		current_profile = Profile.objects.get(user=request.user)
		userform = UserFormProfile(request.POST,instance=request.user)
		profileform = ProfileForm( request.POST , request.FILES ,instance=current_profile)
		if userform.is_valid() and profileform.is_valid():
				userform.save()
				myprofile = profileform.save(commit=False)
				myprofile.user = request.user
				if request.FILES.get('profile_img') != None:
						myprofile.profile_img = request.FILES.get('profile_img')
				myprofile.save()
				return redirect('index')
		context = {
				'userform':userform,
				'profileform':profileform,
		}
		return render(request , 'profile/profile_edit.html' , context )

	def get(self ,request):
			current_profile = Profile.objects.get(user=request.user)
			userform = UserFormProfile(instance=request.user)
			profileform = ProfileForm( instance=current_profile)



			context = {
					'userform':userform,
					'profileform':profileform,
			}
			return render(request , 'profile/profile_edit.html' , context )