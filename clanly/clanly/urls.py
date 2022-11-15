"""clanly URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from app import views


urlpatterns = [
    path("admin/", admin.site.urls),
    path('', views.index, name='index'),
    path('settings/', views.settings, name='settings'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('logout/', views.logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('clan/<int:id>', views.clan, name='clan'),
    path('clan/<int:id>/f', views.follow_clan, name='follow_clan'),
    path('clan/<int:id>/u', views.unfollow_clan, name='unfollow_clan'),
    path('clan/p', views.create_post, name='create_post'),
    path('clan/<int:id>/d', views.delete_post, name='delete_post'),
    path('clan/<int:id>/e', views.edit_post, name='edit_post'),
    path('clan/post/<int:id>/c', views.create_comment, name='create_comment'),
    path('clan/post/<int:id>/d', views.delete_comment, name='delete_comment'),
    path('clan/post/<int:id>/e', views.edit_comment, name='edit_comment'),
    path('myclans/', views.myclans, name='myclans'),
    path('edit_clan/', views.edit_clan, name='edit_clan'),
    path('myclans/', views.myclans, name='delete_clan'),
]       

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
