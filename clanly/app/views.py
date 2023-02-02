from datetime import datetime
from itertools import chain

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, auth
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.messages.storage.fallback import FallbackStorage

from .models import Comment, Community, Post, Profile

# Create your views here.

@login_required(login_url='signin')
def index(request):
    clans = Community.objects.filter(members=request.user)
    posts = Post.objects.all()
    comments = Comment.objects.all()
    return render(request, 'index.html', {'clans': clans, 'posts': posts, 'comments': comments})

def signup(request):

    if not request.user.is_authenticated:
        if request.method == 'POST':
            username = request.POST['username']
            email = request.POST['email']
            fname = request.POST['fname']
            password = request.POST['password']
            password2 = request.POST['password2']

            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username Taken')
                return redirect('signup')

            if len(password2) < 8:
                messages.error(request, 'Password Too Short')
                return redirect('signup')
            elif password == password2:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'Email Taken')
                    return redirect('signup')
                elif User.objects.filter(username=username).exists():
                    messages.error(request, 'Username Taken')
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
                messages.error(request, 'Password Not Matching')
                return redirect('signup')

        else:
            return render(request, 'signup.html')

    else:
        return redirect('/')

def signin(request):

    if not request.user.is_authenticated:

        if request.method == 'POST':
            username = request.POST.get('username', None)
            password = request.POST.get('password', None)

            user = auth.authenticate(username=username, password=password)

            if user:
                auth.login(request, user)
                return redirect('/')
            else:
                messages.info(request, 'Credentials Invalid')
                return redirect('signin')

        else:
            return render(request, 'signin.html')

    else:
        return redirect('/')

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
        password = request.POST.get('password', None)
        password2 = request.POST.get('password2', None)
        password3 = request.POST.get('password3', None)
        changes = False

        if username and username != user.user.username:
            user.user.username = username
            changes = True
        if email and email != user.user.email:
            user.user.email = email
            changes = True
        if fname and fname != user.fname:
            user.fname = fname
            changes = True
        if bio and bio != user.bio:
            user.bio = bio
            changes = True
        if profile_img and profile_img != user.profile_img:
            user.profile_img = profile_img
            changes = True
        if cover_img and cover_img != user.cover_img:
            user.cover_img = cover_img
            changes = True

        if password2:
            if len(password2) < 8:
                messages.info(request, 'Password Too Short')
                return redirect('settings')
            elif password2 == password3:
                messages.info(request, 'Password Changed')
                user.user.set_password(password2)

            else:
                messages.info(request, 'Passwords Not Matching')
                return redirect('settings')
            changes = True
            
        if changes:
            if not password:
                messages.info(request, 'Password Required')
                return redirect('settings')

            if not user.user.check_password(password):
                messages.info(request, 'Password Incorrect')
                return redirect('settings')

        user.user.save()
        user.save()
        
        if password2:
            return redirect('signin')
        return redirect('profile')

    return render(request, 'setting.html', {'user_profile': user})

@login_required(login_url='signin')
def profile(request):
    user = Profile.objects.get(user=request.user)
    clans = Community.objects.filter(members=request.user)
    n_clans = clans.count()

    comments = Comment.objects.filter(user=request.user).count()
    posts = Post.objects.filter(author=request.user).count()
    return render(request, 'profile.html', {'user_profile': user, "clans": clans, "comments": comments, "posts": posts, "n_clans": n_clans})

@login_required(login_url='signin')
def myclans(request):
    clans = Community.objects.filter(admins=request.user)
    return render(request, 'myclans.html', {"clans":clans})

@login_required(login_url='signin')
def clan(request, id=None):
    community = Community.objects.get(id=id)
    posts = Post.objects.filter(community=community)
    n_posts = posts.count()
    followers = len(community.members.all())
    comments = [comment for post in posts for comment in Comment.objects.filter(post=post.id_post)]
    clans = Community.objects.filter(admins=request.user)
    bol = 1
    if request.user in community.members.all():
        bol = 0
    return render(request, 'clan.html', {"followers": followers, "n_posts": n_posts, "id": id, "clan": community, "posts": posts, "comments": comments, "bol": bol, "user": request.user, "clans": clans})

@login_required(login_url='signin')
def follow_clan(request, id=None):
    community = Community.objects.get(id=id)
    community.members.add(request.user)
    community.save()
    return redirect('clan', id=id)

@login_required(login_url='signin')
def unfollow_clan(request, id=None):
    community = Community.objects.get(id=id)
    community.members.remove(request.user)
    community.save()
    return redirect('clan', id=id)

@login_required(login_url='signin')
def update(request, id):
    community = Community.objects.get(id=id)

    if request.method == 'POST':
        description = request.POST.get('content', None)
        communityimg = request.FILES.get('communityimg', None)
        backgroundimg = request.FILES.get('backgroundimg', None)

        if description is not None:
            community.description = description
        if communityimg is not None:
            community.communityimg = communityimg
        if backgroundimg is not None:
            community.background = backgroundimg
        community.updated = datetime.now()
        community.save()
        return redirect('myclans')
    else:
        return redirect('index')

@login_required(login_url='signin')
def edit_clan(request, id):
    clan = Community.objects.get(id=id)
    if request.user not in clan.admins.all():
        return redirect('index')

    return render(request, 'edit_clan.html', {'clan' : clan})


@login_required(login_url='signin')
def create_post(request):
    if request.method == 'POST':
        title = request.POST.get('title', None)
        if not title:
            return redirect('index')
        description = request.POST.get('content', None)
        if not description:
            return redirect('index')
        id = request.POST.get('clan', None)
        if not id:
            return redirect('index')
        community = Community.objects.get(id=id)
        post = Post(title=title, description=description, author=request.user, community=community)
        post.save()
        return redirect('clan', id=id)
    return render(request, 'index')

@login_required(login_url='signin')
def create_comment(request, id=None):
    if request.method == 'POST':
        post = Post.objects.get(id_post=id)
        comment = Comment(content=request.POST.get('content', None), user=request.user, post=post)
        comment.save()
        return redirect('clan', id=post.community.id)

@login_required(login_url='signin')
def create_clan(request):
    if request.method == 'POST':
        name = request.POST.get('name', None)
        description = request.POST.get('content', None)
        if not name:
            messages.info(request, 'Name Required')
            return redirect('create_clan')
        if Community.objects.filter(name=name).exists():
            messages.info(request, 'Clan Already Exists')
            return redirect('create_clan')
        if not description:
            messages.info(request, 'Description Required')
            return redirect('create_clan')
        community = Community.objects.create(name=name, description=description)
        community.save()
        communityimg = request.FILES.get('communityimg', None)
        background = request.FILES.get('background', None)
        if communityimg:
            community.communityimg = communityimg
        if background:
            community.background = background
        community.admins.add(request.user)
        community.members.add(request.user)
        community.save()
        return redirect('clan', id=community.id)
    return render(request, 'create_clan.html')

@login_required(login_url='signin')
def c_clan(request):
    return render(request, 'create_clan.html')

@login_required(login_url='signin')
def delete_clan(request, id=None):
    clan = Community.objects.get(id=id)
    if request.user in clan.admins.all():
        clan.delete()
        return redirect('myclans')
    return redirect('/')

@login_required(login_url='signin')
def delete_post(request, id=None):
    post = Post.objects.get(id_post=id)
    if request.user == post.author:
        community = Community.objects.get(id=post.community.id)
        post.delete()
    return redirect('clan', id=community.id)

@login_required(login_url='signin')
def delete_comment(request, id=None):
    comment = Comment.objects.get(id_comment=id)
    if request.user == comment.user:
        post = Post.objects.get(id_post=comment.post.id_post)
        community = Community.objects.get(id=post.community.id)
        comment.delete()
    return redirect('clan', id=community.id)

@login_required(login_url='signin')
def edit_post(request, id=None):
    post = Post.objects.get(id_post=id)
    if request.user == post.author:
        if request.method == 'POST':
            post.title = request.POST.get('title', None)
            post.description = request.POST.get('content', None)
            post.updated = datetime.now()
            post.save()
            return redirect('clan', id=post.community.id)
        return render(request, 'edit_post.html', {"post": post})
    return redirect('clan', id=post.community.id)

@login_required(login_url='signin')
def edit_comment(request, id=None):
    comment = Comment.objects.get(id_comment=id)
    if request.user == comment.user:
        if request.method == 'POST':
            comment.content = request.POST.get('content', None)
            comment.updated_at = datetime.now()
            comment.save()
            return redirect('clan', id=comment.post.community.id)
        return render(request, 'edit_comment.html', {"comment": comment})
    return redirect('clan', id=comment.post.community.id)

@login_required(login_url='signin')
def create_comment_index(request, id=None):
    if request.method == 'POST':
        post = Post.objects.get(id_post=id)
        comment = Comment(content=request.POST.get('content', None), user=request.user, post=post)
        comment.save()
        return redirect('index')

@login_required(login_url='signin')
def search(request):

    if request.method == 'GET':
        clan_name = request.GET.get('q', '')
        clan_obj = Community.objects.filter(name__icontains=clan_name)

        clans = []
        clans_lst = []

        for c in clan_obj:
            clans.append(c.id)

        for ids in clans:
            clans_ = Community.objects.filter(id=ids)
            clans_lst.append(clans_)

        clans_lst = list(chain(*clans_lst))
    return render(request, 'search.html', {'clans': clans_lst, 'search': clan_name})











