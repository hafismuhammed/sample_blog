from django.urls import path
from . import views


urlpatterns = [
    path('home', views.index, name='home'),
    path('blog', views.blog, name='blog'),
    path('post', views.post, name='post'),
]
