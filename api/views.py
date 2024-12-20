from collections import OrderedDict
import json
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render,redirect

from api.models import AppUser, Hobby
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


def similar_users(request):
    def return_users_with_hobby_count(user_to_compare, current_user, similar_user_count):
        count = 0
        #loop through countign common hobbies
        for utc_hobby in user_to_compare["hobbies"]:
            for cu_hobby in current_user["hobbies"]:
                if utc_hobby == cu_hobby:
                    count +=1 
       
        if count not in similar_user_count:
            similar_user_count[count] = [user_to_compare] # {3: ["Alice"]}
        else:
            similar_user_count[count].append(user_to_compare) # {3: ["Alice", "Bob"]}
            
        return similar_user_count

    similar_user_count = {}
    req_user = request.user
    print("User logged in:", req_user)

    if request.method == "GET":
        #get all users
        users = AppUser.objects.all()
        current_user = AppUser.objects.filter(username=req_user)
        #sort them according to similar hobbies 
        for i in range(len(users)):
            user_to_compare = users[i]
            if user_to_compare != current_user:
                similar_user_count = return_users_with_hobby_count(user_to_compare, current_user, similar_user_count)
        #similar_user_count should look like {3: "David", 7: "Alice", 0: "Charlie"}

        res = OrderedDict()
        res = sorted(similar_user_count.items(), reverse=True) #{3: "David", 7: "Alice", 0: "Charlie"}
        #as a json it will look like [(3, "David"), (7, "Alice"), (0, "Charlie")]
        print(similar_user_count)
    return JsonResponse(json.dumps(similar_user_count), safe=False)