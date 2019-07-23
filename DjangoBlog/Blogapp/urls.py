from django.urls import path,re_path
from Blogapp.views import *

urlpatterns = [
    path('index/',index),
    path('pl/',python_list),
    re_path(r'pl/(?P<p>\d+)',python_list),

    path('ml/',mysql_list),
    re_path(r'ml/(?P<p>\d+)',mysql_list),

    path('ll/',linux_list),
    re_path(r'll/(?P<p>\d+)',linux_list),

    path('dl/',django_list),
    re_path(r'dl/(?P<p>\d+)',django_list),

    path('new/',new),
    path('a/',add_data),

    path('in/', signin),
    path('up/', signup),
    path('upa/', signup_ajax),
    path('upau/', signup_ajax_username),
]
