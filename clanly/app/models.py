from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your models here.


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    bio = models.TextField(blank=True, null=True)
    fname = models.CharField(max_length=20)
    profileimg = models.ImageField(upload_to='profile_images', default='blank-profile-picture.png')
    location = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.user.username


class Community(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    communityimg = models.ImageField(upload_to='community_images', default='blank-profile-picture.png')
    members = models.ManyToManyField(User, related_name='members', blank=True)
    admins = models.ManyToManyField(User, related_name='admins', blank=True)
    banned = models.ManyToManyField(User, related_name='banned', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    postimg = models.ImageField(upload_to='post_images', default='blank-profile-picture.png')
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content


