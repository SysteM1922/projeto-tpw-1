# Generated by Django 4.1.3 on 2023-01-28 16:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Community",
            fields=[
                ("name", models.CharField(max_length=100)),
                ("id_community", models.AutoField(primary_key=True, serialize=False)),
                ("description", models.TextField(blank=True)),
                (
                    "communityimg",
                    models.ImageField(
                        default="blank-profile-picture.png",
                        upload_to="community_images/",
                    ),
                ),
                (
                    "background",
                    models.ImageField(
                        default="blank-profile-picture.png",
                        upload_to="community_images/",
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                ("private", models.BooleanField(default=False)),
                (
                    "admins",
                    models.ManyToManyField(
                        related_name="admins", to=settings.AUTH_USER_MODEL
                    ),
                ),
                (
                    "banned",
                    models.ManyToManyField(
                        blank=True, related_name="banned", to=settings.AUTH_USER_MODEL
                    ),
                ),
                (
                    "members",
                    models.ManyToManyField(
                        related_name="members", to=settings.AUTH_USER_MODEL
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Profile",
            fields=[
                ("id_user", models.IntegerField(primary_key=True, serialize=False)),
                ("bio", models.TextField(blank=True, null=True)),
                ("fname", models.CharField(max_length=30)),
                (
                    "profile_img",
                    models.ImageField(
                        blank=True,
                        default="blank-profile-picture.png",
                        upload_to="profile_images/",
                    ),
                ),
                (
                    "cover_img",
                    models.ImageField(
                        blank=True,
                        default="blank-cover-picture.png",
                        upload_to="cover_images/",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Post",
            fields=[
                ("title", models.CharField(max_length=100)),
                ("id_post", models.AutoField(primary_key=True, serialize=False)),
                ("description", models.TextField(blank=True)),
                (
                    "postimg",
                    models.ImageField(
                        default="blank-profile-picture.png", upload_to="post_images/"
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "community",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="app.community"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Comment",
            fields=[
                ("id_comment", models.AutoField(primary_key=True, serialize=False)),
                ("content", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "post",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="app.post"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
