from django.urls import path

from . import views

urlpatterns = [
    path("authors/", views.get_all_authors, name="get_all_authors"),
    path("authors/<str:author_id>/", views.get_author_by_id, name="get_author_by_id"),
    path("authors/<str:author_id>/followers", views.get_author_by_id_followers, name="get_author_by_id_followers"),
    path("authors/<str:author_id>/followers/<str:foreign_id>", views.get_author_by_id_follower, name="get_author_by_id_follower"),
    path("authors/<str:author_id>/liked", views.get_author_by_id_liked, name="get_author_by_id_liked"),
    path("authors/<str:author_id>/github", views.get_github_activity, name="get_author_by_id_github"),
]
