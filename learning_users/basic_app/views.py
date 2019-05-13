from django.shortcuts import render
from basic_app.forms import UserForm, UserProfileInfoForm

from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
#from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

#ensure view doesnt share a name with imports

def index(request):
    return render(request,'basic_app/index.html')

@login_required
def special(request):
    return HttpResponse("You are logged in, nice!")

#if logged in and user_logout is activated, take me back to index page
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def register(request):
    #check if user is already registered
    registered = False
    #if request is to be posted grab the information off the forms
    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)
        #check if the forms are valid
        if user_form.is_valid() and profile_form.is_valid():
            #if so grab data from the base userform
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            #dont commit to database yet
            #check to see if theres a picture in the form before saving to the database
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']
            profile.save()
            registered = True
        else:
            #if not valid print out errors
            print(user_form.errors,profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()
    return render(request,'basic_app/registration.html',
                            {'user_form':user_form,
                            'profile_form':profile_form,
                            'registered':registered})

def user_login(request):
    #verify the login information has been completed
    if request.method == 'POST':
        #matches to html
        username = request.POST.get('username')
        password = request.POST.get('password')
        #pass variables into authenticate object
        user = authenticate(username=username,password=password)
        #check if the account is active
        if user:
            #if user is active redirect to the home page or else advise user account is not active
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Account not active")

        #else advise account does not exist + advise the incorrect login details
        else:
            print("some tried to login and failed")
            print("Username: {} and password {}".format(username,password))
            return HttpResponse("Invalid login details supplied!")
    #else take me to the login.html page
    else:
        return render(request,'basic_app/login.html',{})
