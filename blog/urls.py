from django.urls import path
from . import views


urlpatterns = [
    path('home', views.index, name='home'),
    path('blog', views.blog, name='blog'),
    path('create_post', views.create_post, name='create_post'),
    path('search/', views.serach, name='search'),
    path('post_detail/<id>', views.post, name='post_detail'),
    path('update/<id>', views.update_post, name='update_post'),
    path('delete/<id>', views.delete_post, name='delete_post'),
]
