from django.urls import path
from . import views

urlpatterns = [
    #path('', views.index, name='index'),
    path('posts/', views.post_endpoint, name='posts'),
    path('posts/<str:post_id>/', views.post_endpoint_id, name='posts_id'), 
    path('posts/<str:post_id>/image', views.get_image_post, name='posts_id_image')
]