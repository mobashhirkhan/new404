from urllib.parse import urlparse

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.db.models import Prefetch
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import DeleteView
from rest_framework.decorators import api_view
from rest_framework.response import Response

from app_posts.models import AppPost
from app_posts.serializers import AppPostSerializer
from authors.models import Author, FriendRequest
from authors.serializers import AuthorSerializer, FriendRequestSerializer
from comments.models import Comment
from comments.serialisers import CommentSerializer
from inboxes.models import Inbox
from likes.models import Like
from likes.serializers import LikeSerializer

from .forms import (
    AppPostForm,
    AuthorEditForm,
    AuthorRegistrationForm,
    CommentForm,
    toCommonMark,
)

# Create your views here.
#####################################################################
"""
functions/views for authors
"""

baseURL_host = "node-net-46d70235bc29.herokuapp.com"
baseURL = f"https://{baseURL_host}/api"


def toTrueID(author_id):
    return f"{baseURL}/authors/{author_id}"


def toUUID(author_id):
    return author_id.split("/")[-1]


# default login view to Login
class AuthorLoginView(LoginView):
    """Login view for author"""

    template_name = "base/login.html"
    fields = "__all__"
    form = AuthorRegistrationForm
    redirect_authenticated_user = True  # authenticated use should not see login page

    def get_success_url(self):
        """Get success url for login"""
        return reverse_lazy("stream")


# function to register author with registration form
def registerAuthor(request):
    """Register author with registration form"""
    if request.method == "POST":
        form = AuthorRegistrationForm(request.POST)
        if form.is_valid():
            author = form.save()

            user = authenticate(
                request,
                username=author.username,
                password=form.cleaned_data["password1"],
            )
            login(request, user)

            # login(
            #     request, author
            # )  # Log in author immediately after registration and send to stream
            return redirect("stream")
    else:
        form = AuthorRegistrationForm()
    return render(request, "base/register.html", {"form": form})


# also add to an inbox as a friend request item
@login_required(login_url="login")  # restrict access to loggedin users
def sendRequest(request, author_id):
    fromAuthor = request.user
    toAuthor = Author.objects.get(id2=author_id)
    # from_id = fromAuthor.id
    print("sendRequest.fromAuthor:", fromAuthor)
    print("sendRequest.toAuthor:", toAuthor)
    print("sendRequest.toAuthor id1:", toAuthor.id)
    print("sendRequest.toAuthor id2:", toAuthor.id2)

    friend_request = FriendRequest.objects.get_or_create(
        fromAuthor=fromAuthor, toAuthor=toAuthor
    )

    # update to friends only in acceped requests

    # update my following
    all_following = fromAuthor.following.all()
    if toAuthor not in all_following:
        fromAuthor.following.add(toAuthor)

    # update thier followers
    all_followers = toAuthor.followers.all()
    if fromAuthor not in all_followers:
        toAuthor.followers.add(fromAuthor)

    # add to the inbox of the toAuthor that fromAuthor wants to connect
    # print("What is toAuthor", toTrueID(toAuthor.id2))
    print("(sendRequest) toTrueID(toAuthor.id2) ->", toTrueID(toAuthor.id2))
    inbox = Inbox.objects.get(author=toTrueID(toAuthor.id2))
    print("(sendRequest) what is inbox 1 ->", type(inbox))
    print("(sendRequest) what is inbox 2 ->", inbox)
    # add friend request to inbox
    friend_request_data = FriendRequestSerializer(friend_request[0]).data
    inbox.friend_requests.append(friend_request_data)
    inbox.save()

    # end of inbox update for a friend request
    fromAuthor.save()
    toAuthor.save()
    print("(sendRequest) what is friend_request object ->", friend_request)
    print("(sendRequest) what is friend_request type ->", type(friend_request[0]))
    return redirect(reverse("get_author", args=[request.user.id2]))


@login_required(login_url="login")  # restrict access to loggedin users
def acceptRequest(request, author_id):
    # print("what is author in accept request", toTrueID(author_id))
    # why are we trying to get FriendRequest while trying to ESTABLISH a friendship?
    new_author_id = toUUID(author_id)
    from_author = Author.objects.get(id2=new_author_id)
    print("(acceptRequest) author_id ->", author_id)
    print("(acceptRequest) What is to author id2 -> request.user.id2", request.user.id2)
    print("(acceptRequest) what is to author id1 -> request.user.id", request.user.id)
    print("(acceptRequest) what is from author id -> from_author.id2", from_author.id2)
    print("(acceptRequest) what is from author id1 -> from_author.id", from_author.id)

    friend_request = FriendRequest.objects.get(
        fromAuthor=from_author, toAuthor=request.user.id
    )
    print("(acceptRequest) what is friend request", friend_request)
    authorA = friend_request.toAuthor
    authorB = friend_request.fromAuthor

    # we follow each other, we are true friends
    Afriends = authorA.friends.all()
    if authorB not in Afriends:
        authorA.friends.add(authorB)
    Bfriends = authorB.friends.all()
    if authorA not in Bfriends:
        authorB.friends.add(authorA)

    # remove from other lists since now true friends
    Afollowing = authorA.following.all()
    if authorB in Afollowing:
        authorA.following.remove(authorB)

    Bfollowers = authorB.followers.all()
    if authorA in Bfollowers:
        authorB.followers.remove(authorA)

    Afollowers = authorA.followers.all()
    if authorB in Afollowers:
        authorA.followers.remove(authorB)

    Bfollowing = authorB.following.all()
    if authorA in Bfollowing:
        authorB.following.remove(authorA)

    authorB.save()
    authorA.save()
    # context = {'author':authorA}
    return redirect(reverse("author_friends", args=[request.user.id2]))


# basically unfollow (when you're not friends yet and stop wanting to follow them)
@login_required(login_url="login")  # restrict access to loggedin users
def unSendRequest(request, author_id):
    # currently logged-in author
    from_author = request.user
    print("(unSendRequest) from_author ->", from_author)
    print("(unSendRequest) author_id ->", author_id)
    unfollow_id = toTrueID(author_id)
    print("(unSendRequest) unfollow_id ->", unfollow_id)
    # author to unfollow
    to_unfollow_author = Author.objects.get(id2=author_id)

    # remove them from my following list
    if to_unfollow_author in from_author.following.all():
        from_author.following.remove(to_unfollow_author)

    # remove me from their followers list
    if from_author in to_unfollow_author.followers.all():
        to_unfollow_author.followers.remove(from_author)

    to_unfollow_author.save()
    from_author.save()
    # redirect to the author's profile page
    return redirect(reverse("get_author", args=[request.user.id2]))


@login_required(login_url="login")  # restrict access to loggedin users
def unBefriend(request, author_id):
    # this is more precisely the relationship ending initiator
    fromAuthor = request.user.id
    toAuthor = Author.objects.get(id2=author_id)
    # friend request to undo
    print("(unBefriend) fromAuthor ->", fromAuthor)
    print("(unBefriend) toAuthor ->", toAuthor)
    print("(unBefriend) toAuthor id2 ->", toAuthor.id2)
    print("(unBefriend) toAuthor id ->", toAuthor.id)
    print("(unBefriend) author_id ->", author_id)
    # fromAuthor will always be the author who initiated the friend request
    # the try-except block is here because exception means that it "could not" find the relationship
    # although the relationship is there and is just the reverse of the one we are looking for
    try:
        friend_request = FriendRequest.objects.get(
            fromAuthor=fromAuthor, toAuthor=toAuthor.id
        )
    except FriendRequest.DoesNotExist:
        # if the friend request does not exist, then it is the other author who initiated the friend request
        friend_request = get_object_or_404(
            FriendRequest, fromAuthor=toAuthor.id, toAuthor=fromAuthor
        )

    # authors involved in the friend request
    author_a = friend_request.toAuthor
    author_b = friend_request.fromAuthor

    # remove from each other's friends list
    if author_b in author_a.friends.all() and author_a in author_b.friends.all():
        author_a.friends.remove(author_b)
        author_b.friends.remove(author_a)

    # any author in friend pair can unBefriend. Once unbefriended, needed to create link again
    # delete the FriendRequest object
    friend_request.delete()

    # redirect to my profile page
    print("(unBefriend) what is request.user.id2 ->", request.user.id2)
    return redirect(reverse("get_author", args=[request.user.id2]))


@login_required(login_url="login")  # restrict access to loggedin users
def getAuthors(request):
    # print(request.user)
    authors = Author.objects.order_by("username")[:15]  # all authors
    following = request.user.following.all()
    friends = request.user.friends.all()
    followers = request.user.followers.all()
    context = {
        "authors": authors,
        "following": following,
        "friends": friends,
        "followers": followers,
    }
    return render(request, "base/authorslist.html", context)


@login_required(login_url="login")  # restrict access to loggedin users
def getAuthorProfile(request, author_id):
    # print(request.user)

    author = Author.objects.get(id2=author_id)  # all post for me and no one else
    followers = author.followers.all()
    following = author.following.all()
    friends = author.friends.all()

    context = {
        "author": author,
        "followers": followers,
        "friends": friends,
        "following": following,
    }
    return render(request, "base/author_detail.html", context)


@login_required(login_url="login")  # restrict access to loggedin users
def editAuthorProfile(request, author_id):
    author_instance = get_object_or_404(Author, id2=author_id)
    allowed = False

    if request.user == author_instance:
        allowed = True
    if request.method == "POST":
        editedProfile = AuthorEditForm(request.POST, instance=author_instance)

        if editedProfile.is_valid():
            # Get the data from the form
            author_data = editedProfile.cleaned_data

            # Create a serializer instance with the data and instance
            serializer = AuthorSerializer(instance=author_instance, data=author_data)

            # Validate and save the data using the serializer
            if serializer.is_valid():
                serializer.save()
                # setting the display name to the new username
                author_instance.displayName = author_data["username"]
                author_instance.save()
                # Redirect to a success page or any other desired page
                return redirect("get_author", author_id)  # success notification maybe

        else:
            return render(
                request,
                "base/editprofile.html",
                {
                    "author_form": editedProfile,
                    "allowed": allowed,
                    "profileid": author_id,
                    "error": editedProfile.errors,
                },
            )

    else:
        newform = AuthorEditForm(instance=author_instance)

    return render(
        request,
        "base/editprofile.html",
        {
            "author_form": newform,
            "allowed": allowed,
            "profileid": author_id,
            "error": None,
        },
    )


@login_required(login_url="login")  # restrict access to loggedin users
def getAuthorFollowers(request, author_id):
    author = Author.objects.get(id2=author_id)
    followers = author.followers.all()
    context = {"author": author, "followers": followers, "author_id": author_id}
    return render(request, "base/author_followers.html", context)


@login_required(login_url="login")  # restrict access to loggedin users
def getAuthorFollowing(request, author_id):
    author = Author.objects.get(id2=author_id)
    following = author.following.all()
    context = {"author": author, "following": following, "author_id": author_id}
    return render(request, "base/author_following.html", context)


@login_required(login_url="login")  # restrict access to loggedin users
def getAuthorFriends(request, author_id):
    author = Author.objects.get(id2=author_id)
    friends = author.friends.all()
    context = {"author": author, "friends": friends, "author_id": author_id}
    return render(request, "base/author_friends.html", context)


#####################################################################


#####################################################################
"""
functions/views for posts
"""


@login_required(login_url="login")
def myUnlistedPost(request):
    """All of my unlisted posts"""
    latest_stream = AppPost.objects.filter(unlisted=True)[:10]
    context = {"latest_stream": latest_stream}
    return render(request, "base/unlisted.html", context)


@login_required(login_url="login")
def getAuthorFriendsThenPostInbox(request, post_id):
    user_id = request.user.id2
    author = Author.objects.get(id2=user_id)
    friends = author.friends.all()

    if request.method == "POST":
        selected_friends = request.POST.getlist("selected_friends")
        print("Friends I selected", selected_friends)
        post = AppPost.objects.get(id2=post_id)
        for friend in selected_friends:
            friend_inbox = Inbox.objects.get(author=friend)
            friend_inbox.posts.append(AppPostSerializer(post).data)
            friend_inbox.save()
        return redirect("stream")
    context = {"author": author, "friends": friends, "author_id": user_id}

    return render(request, "base/share_post_friend_list.html", context)


@login_required(login_url="login")
def stream(request):
    """Stream of posts"""
    latest_stream = (
        AppPost.objects.order_by("-published")
        .filter(visibility="PUBLIC", unlisted=False)[:15]
        .select_related("author")
        .prefetch_related(
            Prefetch(
                "comment_set",
                queryset=Comment.objects.select_related("author").all(),
                to_attr="comments_list",
            )
        )
    )
    context = {"latest_stream": latest_stream, "request": request}
    return render(request, "base/postslist.html", context)


@login_required(login_url="login")
def myPrivatePost(request):
    """All of my private posts"""
    latest_stream = AppPost.objects.order_by("-published").filter(visibility="PRIVATE")[
        :15
    ]

    # get inboxed private posts
    inbox = Inbox.objects.get(author=toTrueID(request.user.id2))
    private_posts = inbox.posts
    for post in private_posts:
        post["id"] = post["id"].rsplit("/", 1)[1]
    context = {"latest_stream": latest_stream, "shared_private_posts": private_posts}
    return render(request, "base/my_private_posts.html", context)


@login_required(login_url="login")
def myFriendsPost(request):
    """All of my friends posts"""
    my_friends = request.user.friends.all()
    latest_stream = AppPost.objects.filter(visibility="FRIENDS").order_by("-published")[
        :15
    ]
    payload = []
    for post in latest_stream:
        if post.author not in my_friends and post.author != request.user:
            continue
        payload.append(post)

    inbox = Inbox.objects.get(author=toTrueID(request.user.id2))
    seriealized_private_posts = inbox.posts
    for post in seriealized_private_posts:
        deserialize_post = AppPostSerializer(data=post)
        if deserialize_post.is_valid():
            post = deserialize_post.save()
            payload.append(post)

    post_form = AppPostForm(user=request.user)
    context = {"latest_stream": payload, "form_to_share": post_form}
    return render(request, "base/friend_posts.html", context)


@login_required(login_url="login")  # restrict access to loggedin users
def postDetail(request, post_id):
    """Post detail"""
    thispost = get_object_or_404(AppPost, id2=post_id)
    context = {"thispost": thispost}
    if request.method == "POST":
        comments = Comment.objects.filter(post=thispost)
        context = {"thispost": thispost, "comments": comments, "form": False}
    else:
        comments = Comment.objects.filter(post=thispost)
        context = {"thispost": thispost, "comments": comments, "form": False}
    return render(request, "base/post_detail.html", context)


@login_required(login_url="login")  # restrict access to loggedin users
def postForm(request):
    """Post form which will be used for creating posts"""
    # fields = ['title','description','contentType','content','categories','visibility']

    print("entered")
    if request.method == "POST":
        print("entered 2")
        post_form = AppPostForm(request.POST, request.FILES, user=request.user)
        if post_form.is_valid():
            post_data = post_form.cleaned_data
            print("post valid")
            # Set the queryset for friends_to_notify field based on the user's friends
            # post_form.fields["friends_to_notify"].queryset = request.user.friends.all()
            for f in request.user.friends.all():
                print("user", f)

            serializer = AppPostSerializer(data=post_data)
            if serializer.is_valid():
                print("serialiser valid")
                post = serializer.save(author=request.user)

                # handle visibility
                # Check if visibility is private
                print("vis is", post.visibility)
                if post.visibility == "PRIVATE":
                    # Get the selected authors from the form
                    friends_to_notify = post_form.cleaned_data.get(
                        "friends_to_notify", []
                    )
                    print("private posts")

                    # Send the post to the inboxes of selected authors
                    for author in friends_to_notify:
                        print(author.username)
                        inbox, wasCreated = Inbox.objects.get_or_create(author=author)
                        inbox.posts.append(serializer.data)
                        inbox.save()

            # Redirect to the page displaying all posts
            return redirect(
                "stream"
            )  # 'stream' is the URL name for the page with all posts
        else:
            print(post_form.errors)
    post_form = AppPostForm(user=request.user)
    # post_form.fields["friends_to_notify"].queryset = request.user.friends.all()
    return render(request, "base/post_form.html", {"post_form": post_form})


@login_required(login_url="login")
def editPostForm(request, post_id):
    post_instance = get_object_or_404(AppPost, id2=post_id)

    # Set queryset for friends_to_notify field
    form = AppPostForm(instance=post_instance, user=request.user)

    if request.method == "POST":
        edited_post = AppPostForm(
            request.POST, instance=post_instance, user=request.user
        )

        if edited_post.is_valid():
            # Get the data from the form
            post_data = edited_post.cleaned_data

            # Create a serializer instance with the data and instance
            serializer = AppPostSerializer(instance=post_instance, data=post_data)

            # Validate and save the data using the serializer
            if serializer.is_valid():
                serializer.save()
                # Redirect to a success page or any other desired page
                return redirect("stream")  # success notification maybe

    return render(request, "base/post_form.html", {"post_form": form})


# whole class just for deleting
class AppPostDeleteView(LoginRequiredMixin, DeleteView):
    """Delete view for post"""

    model = AppPost
    context_object_name = "post"
    success_url = reverse_lazy(
        "stream"
    )  # Redirect to a success page after deletion, success_url_name
    template_name = "base/post_delete.html"

    def get_object(self, queryset=None):
        # Customize this method to retrieve the object based on your requirements
        # In this example, we use 'id2' as the identifier field
        id2 = self.kwargs.get("id2")
        obj = AppPost.objects.get(id2=id2)
        return obj


#####################################################################

#####################################################################
"""
We are going to handle comments now
"""


def comment_display(request, post_id):
    """Display comments on the post and add comments to the post"""
    thispost = get_object_or_404(AppPost, id2=post_id)
    comments = Comment.objects.filter(post=thispost)
    if request.method == "POST":
        # inbox = Inbox.objects.get(author=thispost.author)
        form = CommentForm(request.POST)
        if form.is_valid():
            clean_data = form.cleaned_data
            serialiser = CommentSerializer(data=clean_data)
            my_summary = f"{request.user.username} commented '{clean_data.get('content')}'on your post '{thispost.title}'"
            if serialiser.is_valid():
                serialiser.save(
                    author=request.user,
                    post=get_object_or_404(AppPost, id2=post_id),
                    summary=my_summary,
                )
                if request.user != thispost.author:
                    inbox = Inbox.objects.get(author=thispost.author)
                    inbox.comments.append(serialiser.data)
                    inbox.save()
                # inbox.comments.append(serialiser.data)
            # update post count
            post = AppPost.objects.get(id2=post_id)
            post.count += 1
            post.save()
            # inbox.save()
            return redirect(
                "get_post", post_id
            )  # 'get_post' is the URL name for the page with all posts
    else:
        form = CommentForm()

    # return render(request, "base/new_comment.html", {"form": form, "post_id": post_id})
    return render(
        request,
        "base/post_detail.html",
        {"thispost": thispost, "comments": comments, "form": form},
    )


@login_required(login_url="login")  # restrict access to loggedin users
def comment_edit(request, post_id, comment_id):
    """Updates the comment"""
    thispost = get_object_or_404(AppPost, id2=post_id)
    comments = Comment.objects.filter(post=thispost)
    comment_instance = get_object_or_404(Comment, id2=comment_id)
    if request.method == "POST":
        to_be_edited_comment = CommentForm(request.POST, instance=comment_instance)
        if to_be_edited_comment.is_valid():
            comment_data = to_be_edited_comment.cleaned_data
            serialiser = CommentSerializer(instance=comment_instance, data=comment_data)

            if serialiser.is_valid():
                serialiser.save()
                return redirect("get_post", post_id)
    else:
        to_be_edited_comment = CommentForm(instance=comment_instance)

    return render(
        request,
        "base/post_detail.html",
        {"thispost": thispost, "comments": comments, "form": to_be_edited_comment},
    )


@login_required(login_url="login")  # restrict access to loggedin users
def delete_comment(request, post_id, comment_id):
    """Deletes the comment."""
    comment_instance = get_object_or_404(Comment, id2=comment_id)
    post = AppPost.objects.get(id2=post_id)
    allowed = False
    if request.user == comment_instance.author or request.user == post.author:
        allowed = True
    if request.method == "POST":
        comment_instance.delete()
        post.count -= 1
        post.save()
        return redirect("get_post", post_id)

    return render(
        request,
        "base/delete_comment.html",
        {"post_id": post_id, "allowed": allowed, "comment": comment_instance},
    )


@login_required(login_url="login")  # restrict access to loggedin users
def like_comment(request, post_id, comment_id):
    """Likes the comment."""
    comment_instance = get_object_or_404(Comment, id2=comment_id)
    post = AppPost.objects.get(id2=post_id)
    # if request.method == "POST":
    # like_summary = "Your comment "+ comment_instance.content + "liked by " + request.user.username
    like_summary = (
        f"{request.user.username} liked your comment '{comment_instance.content}'"
    )
    print(like_summary)
    inbox = Inbox.objects.get(author=comment_instance.author)
    if not Like.objects.filter(
        author=request.user, object_on=comment_instance.id
    ).exists():
        my_author = Author.objects.get(id2=request.user.id2)
        # print(f"name is {my_author.displayName} with id {my_author.id2}")
        like = Like.objects.create(
            author=my_author,
            summary=like_summary,
            object_on=comment_instance.id,
            object_type="comment",
        )
        if request.user != comment_instance.author:
            like_data = LikeSerializer(like).data
            inbox.likes.append(like_data)
            inbox.save()
        comment_instance.liked.add(like)
        comment_instance.save()
        print(request.user.id)
        return redirect("get_post", post_id)
    else:
        return render(request, "base/already_liked.html", {"post_id": post_id})


@login_required(login_url="login")
def like_post(request, post_id):
    """Likes the post."""
    post_instance = get_object_or_404(AppPost, id2=post_id)
    like_summary = f"{request.user.username} liked your post '{post_instance.title}'"
    print(like_summary)
    inbox = Inbox.objects.get(author=post_instance.author)
    if not Like.objects.filter(
        author=request.user, object_on=post_instance.id
    ).exists():
        my_author = Author.objects.get(id2=request.user.id2)
        like = Like.objects.create(
            author=my_author,
            summary=like_summary,
            object_on=post_instance.id,
            object_type="post",
        )
        if request.user != post_instance.author:
            like_data = LikeSerializer(like).data
            inbox.likes.append(like_data)
            inbox.save()
        post_instance.liked.add(like)
        post_instance.save()
        return redirect("get_post", post_id)
    else:
        return render(request, "base/already_liked.html", {"post_id": post_id})


#####################################################################

#####################################################################
"""
We are going to handle inbox after this line
"""


@login_required(login_url="login")  # restrict access to loggedin users
def displayInbox(request, author_id):
    """Display inbox"""
    # inbox = Inbox.objects.get(author=request.user)
    # posts = inbox.posts
    # context = {"posts": posts}
    # return render(request, "base/inbox.html", context)
    # -------
    # thispost = get_object_or_404(AppPost, id=post_id)
    print("(displayInbox) toTrueID(author_id) ->", toTrueID(author_id))
    inbox = Inbox.objects.get(author=toTrueID(author_id))
    posts = inbox.posts
    f_req = inbox.friend_requests
    likes = inbox.likes
    comments = inbox.comments
    items = posts + likes + comments + f_req
    # items = sorted(items, key=lambda item: item["published"], reverse=True)

    return render(request, "base/inbox.html", {"items": items})
