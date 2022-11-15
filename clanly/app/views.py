from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import HttpResponse

from .models import Profile, Community, Comment, Post
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
                user = User.objects.create_user(username=username, email=email, password=password)
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
                auth.login(request, user)
                return redirect('/')
            else:
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
            user.fname = fname
        if bio is not None:
            user.bio = bio
        if profile_img is not None:
            user.profile_img = profile_img
        if cover_img is not None:
            user.cover_img = cover_img


        if user.user.check_password(request.POST.get("password", None)):
            password2 = request.POST.get('password2', None)
            password3 = request.POST.get('password3', None)
            if password2 == password3:
                messages.info(request, 'Password Changed')
                user.user.set_password(password2)
            else:
                messages.info(request, 'Passwords Not Matching')
                return redirect('settings')

        user.user.save()
        user.save()
        
        return redirect('settings')

    return render(request, 'setting.html', {'user_profile': user})

@login_required(login_url='signin')
def profile(request):
    user = Profile.objects.get(user=request.user)
    clans = Community.objects.filter(members=request.user).count()

    comments = Comment.objects.filter(user=request.user).count()
    posts = Post.objects.filter(author=request.user).count()
    return render(request, 'profile.html', {'user_profile': user, "clans": clans, "comments": comments, "posts": posts})

@login_required(login_url='signin')
def clan(request):
    return render(request, 'clan.html')

@login_required(login_url='signin')
def myclans(request):
    return render(request, 'myclans.html')

<<<<<<< HEAD
@login_required(login_url='signin')
def clan(request, id=None):
    community = Community.objects.get(id_community=id)
    posts = Post.objects.filter(community=community).count()
    followers = len(community.members.all())
    return render(request, 'clan.html', {"followers": followers, "posts": posts, "id": id, "clan": community})

@login_required(login_url='signin')
def follow_clan(request, id=None):
    community = Community.objects.get(id_community=id)
    community.members.add(request.user)
    community.save()
    return redirect('clan', id=id)

@login_required(login_url='signin')
def unfollow_clan(request, id=None):
    community = Community.objects.get(id_community=id)
    community.members.remove(request.user)
    community.save()
    return redirect('clan', id=id)

=======
def edit_clan(request):
    return render(request, 'edit_clan.html')
>>>>>>> 3192d6d43fc02890b0256b477a2016380cc69ad7












