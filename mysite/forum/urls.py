"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from django.conf.urls import url, include
from django.views.generic import ListView, DetailView
from forum.models import *
from . import views

urlpatterns = [
    url(r'^reply/(\d+)/$', views.post_reply, name='reply'),
    url(r'^upvote/(\d+)/(\d+)$', views.upvote),
    url(r'^(\d+)/$', views.topic, name='topic-detail'),
    url(r'^addpro/(\d+)$', views.addpro),
    url(r'^addcon/(\d+)$', views.addcon),
    url(r'^pdf/(\d+)$', views.pdf),
    url(r'^delete/(\d+)/(\d+)$', views.deleteComment),
]
