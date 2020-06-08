from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
    #Api for post comment
    path('postcomment',views.postcomment,name="postcomment"),
    
    path('', views.bloghome, name='bloghome'),
    path('<str:slug>', views.blogpost, name='blogpost'),
   
    
]