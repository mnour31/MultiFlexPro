from django.contrib.auth.models import User
from users.models import Profile
from .models import Info

def my_context(request):
    user = request.user
    try:
        profile = Profile.objects.get(user=user)
    except:
        profile = None
    info = Info.objects.all().first()

    context = {
        'user_Profile':profile,
        'info':info,
         }
    return context