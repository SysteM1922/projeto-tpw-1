from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import HttpResponse

from .models import Profile
from django.contrib.auth.decorators import login_required


# Create your views here.

@login_required(login_url='signin')
def index(request):
    return render(request, 'index.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        fname = request.POST['fname']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                print("email taken")
                messages.info(request, 'Email Taken')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                print("username taken")
                messages.info(request, 'Username Taken')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password, first_name=fname)
                user.save()

                # create a Profile object for the new user
                profile = Profile(user=user, id_user=user.id, fname=fname)
                profile.save()

                messages.info(request, 'User Created')
                return redirect('signin')
        else:
            messages.info(request, 'Password Not Matching')
            return redirect('signup')
        
    else:
        return render(request, 'signup.html')

def signin(request):

    if not request.user.is_authenticated:

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

    else:
        return redirect('settings')

@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')

@login_required(login_url='signin')
def settings(request):
    user = Profile.objects.get(user=request.user)

    if request.method == 'POST':

        username = request.POST.get('username', None)
        email = request.POST.get('email', None)
        fname = request.POST.get('name', None)
        bio = request.POST.get('bio', None)
        profile_img = request.FILES.get('profile_img', None)
        cover_img = request.FILES.get('cover_img', None)

        if username is not None:
            user.user.username = username
        if email is not None:
            user.user.email = email
        if fname is not None:
            user.user.first_name = fname
        if bio is not None:
            user.bio = bio
        if profile_img is not None:
            user.profile_img = profile_img
        if cover_img is not None:
            user.cover_img = cover_img

        user.user.save()
        user.save()
        
        return redirect('settings')

    return render(request, 'setting.html', {'user_profile': user})

@login_required(login_url='signin')
def profile(request):
    user = request.user
    return render(request, 'profile.html', {'user_profile': user})

def clan(request):
    return render(request, 'clan.html')













