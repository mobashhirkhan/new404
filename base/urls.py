from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from django.urls import path

from authors.views import get_github_activity
from inboxes import views as inbox_views

from . import views

urlpatterns = [
    path("register/", views.registerAuthor, name="register"),
    path("login/", views.AuthorLoginView.as_view(), name="login"),
    path(
        "logout/", LogoutView.as_view(next_page="login"), name="logout"
    ),  # just need to send get request and a redirect as arg, no need for customisation
    path("", views.stream, name="stream"),
    path(
        "authors/<str:author_id>/github_activity/",
        get_github_activity,
        name="github_activity",
    ),
    path(
        "authors/<str:author_id>/edit-profile/",
        views.editAuthorProfile,
        name="edit_profile",
    ),
    path("posts/<str:post_id>/", views.postDetail, name="get_post"),
    path("new-post/", views.postForm, name="new_post"),
    path("edit-post/<str:post_id>/", views.editPostForm, name="edit_post"),
    path(
        "delete-post/<str:id2>/", views.AppPostDeleteView.as_view(), name="del_post"
    ),  # need pk specifically for delete
    path("private/", views.myPrivatePost, name="private_posts"),
    path("friend-posts/", views.myFriendsPost, name="friends_posts"),
    path("posts/<str:post_id>/comment", views.comment_display, name="comment_display"),
    path(
        "posts/<str:post_id>/comment/<str:comment_id>/edit",
        views.comment_edit,
        name="comment_edit",
    ),
    path(
        "posts/<str:post_id>/comment/<str:comment_id>/delete",
        views.delete_comment,
        name="comment_delete",
    ),
    path("unlisted/", views.myUnlistedPost, name="unlisted_posts"),
    path(
        "share-post-friends/<str:post_id>/",
        views.getAuthorFriendsThenPostInbox,
        name="share_post_friends",
    ),
    path(
        "posts/<str:post_id>/comment/<str:comment_id>/like",
        views.like_comment,
        name="comment_like",
    ),
    path("posts/<str:post_id>/like", views.like_post, name="post_like"),
    path("befriend-author/<str:author_id>/", views.sendRequest, name="befriend_author"),
    path(
        "befriend-author-back/<str:author_id>/",
        views.acceptRequest,
        name="befriend_author_back",
    ),
    path(
        "unfollow/<uuid:author_id>/", views.unSendRequest, name="unfollow_author"
    ),  # unfollow someone you're following
    path(
        "unbefriend/<uuid:author_id>/", views.unBefriend, name="unbefriend_author"
    ),  # unfriend
    path("authors/", views.getAuthors, name="authors"),
    path("authors/<uuid:author_id>/", views.getAuthorProfile, name="get_author"),
    path(
        "authors/<str:author_id>/followers",
        views.getAuthorFollowers,
        name="author_followers",
    ),
    path(
        "authors/<str:author_id>/inbox",
        views.displayInbox,
        name="author_inbox",
    ),
    path(
        "authors/<str:author_id>/following",
        views.getAuthorFollowing,
        name="author_following",
    ),
    path(
        "authors/<str:author_id>/friends", views.getAuthorFriends, name="author_friends"
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
