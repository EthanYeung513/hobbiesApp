from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render

from api.forms import AppUserSignUpForm
from .models import AppUser
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required


def main_spa(request: HttpRequest) -> HttpResponse:
    return render(request, 'api/spa/index.html', {})

def sign_up(request):
    if request.method == 'POST':
        form = AppUserSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) 
            return redirect('api/spa/index.html')  
    else:
        form = AppUserSignUpForm()
    