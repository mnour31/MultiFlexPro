from django.urls import path
from .views import Register , login_request , ProfileView , logout_request , ProfileEdit
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('register' , Register.as_view() , name='register' ),
    path('login' , login_request , name='login' ),
    path("logout", logout_request, name= "logout"),
    path('<slug:slug>' , ProfileView.as_view() , name='profile-detail' ),
    path('profile/edit' , ProfileEdit.as_view() , name='profile-edit' ),

]