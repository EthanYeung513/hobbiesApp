from collections import OrderedDict
import json
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required

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

@login_required
def similar_users(request):
    def return_users_with_hobby_count(user_to_compare, current_user, similar_user_count):
        count = 0
        #loop through countign common hobbies
        user_to_compare_hobbies = user_to_compare.hobbies.all()
        current_user_hobbies = current_user.hobbies.all()   

        for utc_hobby in user_to_compare_hobbies:
            for cu_hobby in current_user_hobbies:
                if utc_hobby == cu_hobby:
                    count +=1 

        # convert the info of the user compared into dict
        # this prevents the user object from being serialized
        # allowing the json response to be serialized instead
        user_data = {
            "username": user_to_compare.username,
            "hobbies": list(user_to_compare_hobbies.values_list("hobby_name", flat=True)),
        }

        # save the user data to a dictionary which counts how many common hobbies each user has
        if count not in similar_user_count:
            similar_user_count[count] = [user_data] # {3: ["Alice"]}
        else:
            similar_user_count[count].append(user_data) # {3: ["Alice", "Bob"]}
            
        return similar_user_count

    # START OF FUNCTION
    similar_user_count = {}
    req_user = request.user
    print("User logged in:", req_user)

    if request.method == "GET":
        #get QerySet object of current user
        try:
            current_user = AppUser.objects.get(username=req_user)
        except AppUser.DoesNotExist:
            return JsonResponse({"error": "Logged-in user not found"}, status=404)

        #get all users except current user
        users = AppUser.objects.exclude(username=req_user.username)

        #sort them according to similar hobbies 
        for user_to_compare in users:
            similar_user_count = return_users_with_hobby_count(user_to_compare, current_user, similar_user_count)
        #similar_user_count should look like {3: "David", 7: "Alice", 0: "Charlie"}

        res = OrderedDict(sorted(similar_user_count.items(), reverse=True)) #{3: "David", 7: "Alice", 0: "Charlie"}
        #as a json it will look like [(3, "David"), (7, "Alice"), (0, "Charlie")]
        print("result dict:", similar_user_count)
    return JsonResponse(similar_user_count, safe=False)