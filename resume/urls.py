from django.urls import path 
from .views import CreateCv , CvManage , ViewCv , job_title , skilles , experience , services , portfolio , testimonial , mysend_mail
from django.contrib.auth.decorators import login_required
urlpatterns = [
    path('' , login_required( CreateCv.as_view() , login_url='login')  , name='create-cv'),
    path('cv-manage' , login_required( CvManage.as_view() , login_url='login')  , name='cv_manage'),

    path('<str:slug>/<int:id>' , ViewCv.as_view() , name='view_cv'),

    path('cv-manage/job-title' , job_title , name='job-title'),
    path('cv-manage/skilles' , skilles , name='skilles'),
    path('cv-manage/experience' , experience , name='experience'),
    path('cv-manage/services' , services , name='services'),
    path('cv-manage/portfolio' , portfolio , name='portfolio'),
    path('cv-manage/testimonial' , testimonial , name='testimonial'),

    path('send-email-cv',mysend_mail , name='send_email_cv'),


]