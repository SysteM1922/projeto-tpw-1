from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, auth
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .models import Comment, Community, Post, Profile

# Create your views here.

@login_required(login_url='signin')
def index(request):
    clans = Community.objects.filter(members=request.user)
    posts = Post.objects.all()
    comments = Comment.objects.all()
    return render(request, 'index.html', {'clans': clans, 'posts': posts, 'comments': comments})

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
def clan(request, id=None):
    community = Community.objects.get(id_community=id)
    posts = Post.objects.filter(community=community)
    n_posts = posts.count()
    followers = len(community.members.all())
    comments = [comment for post in posts for comment in Comment.objects.filter(post=post.id_post)]
    clans=Community.objects.filter(members=request.user)
    bol = 1
    if request.user in community.members.all():
        bol = 0
    return render(request, 'clan.html', {"followers": followers, "n_posts": n_posts, "id": id, "clan": community, "posts": posts, "comments": comments, "bol": bol, "user": request.user, "clans": clans})

@login_required(login_url='signin')
def myclans(request):
    clans = Community.objects.filter(admins=request.user)
    return render(request, 'myclans.html', {"clans":clans})

@login_required(login_url='signin')
def clan(request, id=None):
    community = Community.objects.get(id_community=id)
    posts = Post.objects.filter(community=community)
    n_posts = posts.count()
    followers = len(community.members.all())
    comments = [comment for post in posts for comment in Comment.objects.filter(post=post.id_post)]
    clans=Community.objects.filter(admins=request.user)
    print(clans)
    bol = 1
    if request.user in community.members.all():
        bol = 0
    return render(request, 'clan.html', {"followers": followers, "n_posts": n_posts, "id": id, "clan": community, "posts": posts, "comments": comments, "bol": bol, "user": request.user, "clans": clans})

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

@login_required(login_url='signin')
def edit_clan(request):
    return render(request, 'edit_clan.html')

@login_required(login_url='signin')
def create_post(request):
    if request.method == 'POST':
        title = request.POST.get('title', None)
        description = request.POST.get('content', None)
        id = request.POST.get('clan', None)
        community = Community.objects.get(id_community=id)
        post = Post(title=title, description=description, author=request.user, community=community, created=datetime.now(), updated=datetime.now())
        post.save()
        return redirect('clan', id=id)
    return render(request, 'create_post.html')

@login_required(login_url='signin')
def create_comment(request, id=None):
    if request.method == 'POST':
        post = Post.objects.get(id_post=id)
        comment = Comment(content=request.POST.get('content', None), user=request.user, post=post, created_at=datetime.now(), updated_at=datetime.now())
        comment.save()
        return redirect('clan', id=post.community.id_community)

@login_required(login_url='signin')
def create_clan(request):
    if request.method == 'POST':
        name = request.POST.get('name', None)
        description = request.POST.get('content', None)
        communityimg = request.FILES.get('communityimg', None)
        background = request.FILES.get('background', None)
        community = Community.objects.create(name=name, description=description, communityimg=communityimg, background=background, created=datetime.now(), updated=datetime.now(), private=False)
        community.save()
        community.admins.add(request.user)
        community.save()
        return redirect('clan', id=community.id_community)

@login_required(login_url='signin')
def delete_clan(request, id=None):
    community = Community.objects.get(id_community=id)
    if request.user == community.admin:
        community.delete()
        return redirect('index')
    return redirect('clan', id=id)

@login_required(login_url='signin')
def delete_post(request, id=None):
    post = Post.objects.get(id_post=id)
    if request.user == post.author:
        community = Community.objects.get(id_community=post.community.id_community)
        post.delete()
    return redirect('clan', id=community.id_community)

@login_required(login_url='signin')
def delete_comment(request, id=None):
    comment = Comment.objects.get(id_comment=id)
    if request.user == comment.user:
        post = Post.objects.get(id_post=comment.post.id_post)
        community = Community.objects.get(id_community=post.community.id_community)
        comment.delete()
    return redirect('clan', id=community.id_community)

@login_required(login_url='signin')
def edit_post(request, id=None):
    pass

@login_required(login_url='signin')
def edit_comment(request, id=None):
    pass

@login_required(login_url='signin')
def create_comment_index(request, id=None):
    if request.method == 'POST':
        post = Post.objects.get(id_post=id)
        comment = Comment(content=request.POST.get('content', None), user=request.user, post=post, created_at=datetime.now(), updated_at=datetime.now())
        comment.save()
        return redirect('index')














