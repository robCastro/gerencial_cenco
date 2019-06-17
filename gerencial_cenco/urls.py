"""gerencial_cenco URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include
from django.contrib.auth import views as auth_views
from apps_cenco.login.views import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^director/', include('apps_cenco.director.urls')),
    url(r'^profesor/', include('apps_cenco.profesor.urls')),
    url(r'^supervisor/', include('apps_cenco.supervisor.urls')),
    url(r'^accounts/login/$', auth_views.login,{'template_name': 'Login/login.html'}, name='login' ),
    url(r'^logout/$', auth_views.logout, {'template_name': 'Login/logout.html'}, name='logout'),
    url(r'^$', principal, name="inicio"),
]
