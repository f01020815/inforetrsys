# -*- coding:utf-8 -*-
# Author: Li Gaoyang<gylia@isoftstone.com>
"""searching URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
1"""
from django.urls import path
from userworkstation import views

urlpatterns = [
    path('feedback/', views.feedback),
    path('insert/', views.insert),

    path('', views.index),
    path('index/', views.index),
    path('show/', views.show),

    # add by wangshibin 20190722
    path('deletepathid/', views.delete_path_id),

    # add by wangshibin 20190725
    path('update/', views.update),
    path('download_file/', views.download_file),
    # path('delete_file/', views.delete_file),  del by wangshibin 20190929

    # add by zhangxiaoming   20190814
    path('rollback/', views.rollback),
    path('login/', views.login),
    path('register/', views.register),
    path('document_show/', views.document_show),
    path('register_user/', views.register_user),
]
