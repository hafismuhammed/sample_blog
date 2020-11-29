from django.urls import path
from . import views


urlpatterns = [
   # path('home', views.index, name='home'),
    path('home', views.IndexView.as_view(), name='home'),
    #path('blog', views.post_list, name='blog'),
    path('blog', views.PostListView.as_view(), name='blog'),
    #path('create_post', views.post_create, name='create_post'),
    path('create_post', views.PostCreateView.as_view(), name='create_post'),
    #path('search/', views.serach, name='search'),
    path('search/', views.SerachView.as_view(), name='search'),
    #path('post_detail/<id>', views.post_detail, name='post_detail'),
    path('post_detail/<pk>', views.PostDetailView.as_view(), name='post_detail'),
   #path('update/<id>', views.post_update, name='update_post'),
    path('update/<pk>', views.PostUpdateView.as_view(), name='update_post'),
    #path('delete/<id>', views.post_delete, name='delete_post'),
    path('delete/<pk>', views.PostDeleteView.as_view(), name='delete_post'),
]
