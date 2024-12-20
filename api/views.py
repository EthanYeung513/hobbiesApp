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
    def count_same_hobbies(user1, user2, freq, seen_pairs):
        count = 0
        #loop through countign common hobbies
        for h1 in user1["hobbies"]:
            for h2 in user2["hobbies"]:
                if h1 == h2:
                    count +=1 

        # Create a frozenset to represent the user pair (unordered)
        pair = frozenset([user1["username"], user2["username"]])
        
        # Check if the pair has already been processed
        if pair not in seen_pairs:
            # If not, add to the seen pairs set
            seen_pairs.add(pair)
            
            # Get the existing list of user pairs for the given count or create an empty list
            freq_value = freq.get(count, [])
            
            # Add the pair to the list
            freq_value.append([user1, user2])
            
            # Update the dictionary with the new pair list
            freq[count] = freq_value
        
        return freq, seen_pairs
    
    freq = {}
    seen_pairs = set()
    if request.method == "GET":
        #get all users
        users = AppUser.objects.all()
        #sort them according to similar hobbies 
        for i in range(len(users)):
            a = users[i]
            for u in users:
                if a != u:
                    freq, seen_pairs = count_same_hobbies(a, u, freq, seen_pairs)
        
        # res_array - [(7, ['e', 'j']), (3, ['a', 'b']), (0, [])]
        # res_array[0] - (7, ['e', 'j'])
        # res_array[0][0] - 7
        
        # we don't need to know specifically how many hobbies are shared
        # so just return a list of users in order
        res = OrderedDict()
        res = sorted(freq.items(), reverse=True)

        # print(res)
        # print()
        # print(res[0]) # (3, [['Alice', 'David'], ['Alice', 'Hank'], ['Bob', 'Hank'], ['David', 'Frank'], ['David', 'Hank']])
        # print(res[0][1]) # [['Alice', 'David'], ['Alice', 'Hank'], ['Bob', 'Hank'], ['David', 'Frank'], ['David', 'Hank']]
        # print(res[0][1][2]) # ['Bob', 'Hank']
        
        
        print(freq)
    return JsonResponse(json.dumps(freq), safe=False)