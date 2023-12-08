from django.urls import path
from . import views


urlpatterns = [
    path('likes/', views.likePosts, name='likes'),
    path('comments/<str:comment_id>/likes/', views.likeComments, name='likes')
]
