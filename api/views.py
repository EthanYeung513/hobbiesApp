from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render,redirect
from .forms import AppUserSignUpForm

def main_spa(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        return render(request, 'api/spa/index.html', {})
    else:
        return redirect('signup')  


def signup(request):
    if request.method == "POST":
        form = AppUserSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            #return redirect('login')  
    else:
        form = AppUserSignUpForm()
    
    return render(request, 'api/spa/signup.html', {'form': form})