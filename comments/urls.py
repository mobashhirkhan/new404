from django.urls import path
from . import views

urlpatterns = [
    path('comments/', views.comment_endpoint, name='comments'),
    path('comments/<str:comment_id>/', views.comment_endpoint_id, name='comments_id'), 
]