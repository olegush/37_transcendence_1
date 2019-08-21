from django.conf import settings
from django.shortcuts import render, redirect

def index(request):
    if request.user.is_authenticated:
        return redirect('wall/')
    return render(request, 'registration/login.html')
