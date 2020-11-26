from django.urls import path
from . import views


urlpatterns = [
    path('home', views.index, name='home'),
    path('blog', views.blog, name='blog'),
    path('search/', views.serach, name='search'),
    path('post_detail/<id>', views.post, name='post_detail'),
]
