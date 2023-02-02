from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()
# Create your models here.

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField(primary_key=True)
    bio = models.TextField(blank=True, default='Hi, I am using Clanly!')
    fname = models.CharField(max_length=30)
    profile_img = models.ImageField(blank=True, upload_to='images/profile_images/', default='images/defaults/no-profile.png')
    cover_img = models.ImageField(blank=True, upload_to='images/cover_images/', default='images/defaults/no-background.png')

    def __str__(self):
        return self.user.username


class Community(models.Model):
    name = models.CharField(max_length=100)
    id = models.AutoField(primary_key=True)
    description = models.TextField(blank=True)
    communityimg = models.ImageField(blank=True, upload_to='images/community_images/', default='images/defaults/no-clan.png')
    background = models.ImageField(blank=True, upload_to='images/community_images/', default='images/defaults/no-background.png')
    members = models.ManyToManyField(User, related_name='members')
    admins = models.ManyToManyField(User, related_name='admins')

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=100)
    id_post = models.AutoField(primary_key=True)
    description = models.TextField(blank=True)
    postimg = models.ImageField(blank=True, upload_to='images/post_images/', default='images/defaults/no-background.png')
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    id_comment = models.AutoField(primary_key=True)
    content = models.TextField()

    def __str__(self):
        return self.content


