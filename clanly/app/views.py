from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import HttpResponse

from .models import Profile
from django.contrib.auth.decorators import login_required


# Create your views here.

def index(request):
    return render(request, 'index.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        fname = request.POST['fname']
        password = request.POST['password']

        if password:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password, first_name=fname)
                user.save()

                # log user in and redirect to settings page
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)

                # create a Profile object for the new user
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id, fname=fname)
                new_profile.save()


                return redirect('settings')
        else:
            messages.info(request, 'Password Not Matching')
            return redirect('signup')
        
    else:
        return render(request, 'signup.html')

def signin(request):
    
    if request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            print("user : ", user)
            auth.login(request, user)
            return redirect('/')
        else:
            print("invalid")
            messages.info(request, 'Credentials Invalid')
            return redirect('signin')

    else:
        return render(request, 'signin.html')

@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')


def settings(request):
    user = request.user
    #print("user : ", user)

    if request.method == 'POST':
        #print("in")
        if request.FILES.get('image') == None:
            #print("in2")
            bio = request.POST.get('bio', None)
            location = request.POST.get('location', None)
            fname = request.POST.get('fname', "teste")

            #user.profileimg = image
            user.bio = bio
            user.fname = fname
            user.location = location
            user.save()

        if request.FILES.get('image') != None:
            #print("in3")
            bio = request.POST['bio']
            location = request.POST['location']
            fname = request.POST['fname']
            #print("user2 : ", user)
            #user.profileimg = image
            user.bio = bio
            user.location = location
            user.save()
        
        return redirect('settings')
    #print("user3 : ", user)
    return render(request, 'setting.html', {'user_profile': user})


def profile(request):
    user = request.user
    return render(request, 'profile.html', {'user_profile': user})

def login(request):
    return render(request, 'login.html')
















