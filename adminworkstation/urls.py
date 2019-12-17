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
from adminworkstation import views

urlpatterns = [
    path('admingo/', views.admingo),

    # add by wangshibin 20190723
    path('approval/', views.approval),
    path('agree/', views.agree),
    path('reject/', views.reject),
    path('feedback_show/', views.feedback_show),
    path('deletefeedback/', views.feedback_del),
    path('log_show/', views.log_show),
    path('export_excel/', views.export_excel),

    #add by xiaoming 20190930
    path('maintenance/', views.maintenance),
    path('log_filter/', views.log_filter),
    path('user_management/', views.user_management),
    path('deleteuser/', views.user_del),
    path('user_approval/', views.user_approval),
    path('agree_user/', views.agree_user),
    path('reject_user/', views.reject_user),

]
