from django.http import HttpRequest
from django.shortcuts import render
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from authors.models import Author
from inboxes.models import Inbox
from inboxes.serializers import InboxSerializer
from likes.serializers import LikeSerializer

# Create your views here.

# URL: ://service/authors/{AUTHOR_ID}/inbox
allowed = ["GET", "POST", "DELETE"]


baseURL_host = "connection-net-e444016a9ef0.herokuapp.com"
baseURL = f"https://{baseURL_host}/api"

def toTrueIDAuthor(author_id):
    return f"{baseURL}/authors/{author_id}"

def getAll(request, author_id):
    try:
        author = Author.objects.get(id=author_id)
    except Author.DoesNotExist:
        out = {"status": 1, "message": "Author not found"}
        return Response(out, status.HTTP_404_NOT_FOUND)

    try:
        inbox = Inbox.objects.get(author=author_id)
    except Inbox.DoesNotExist:
        out = {"status": 1, "message": "Author Inbox could not be found"}
        return Response(out, status.HTTP_404_NOT_FOUND)

    # Serialize the inbox
    inbox_serializer = InboxSerializer(inbox)

    # Combine all items into a single list
    posts = inbox.posts if inbox.posts else []
    friend_requests = inbox.friend_requests if inbox.friend_requests else []
    likes = inbox.likes if inbox.likes else []
    comments = inbox.comments if inbox.comments else []
    items = posts + friend_requests + likes + comments

    # Serialize the combined list and send it as a response
    out = {"type": "Inbox", "author": author_id, "items": items}
    return Response(out)


# call this every time any action is performed that should go into the inbox
# actions that will be in the inbox are: friend requests, likes, comments, posts
def addItem(request, author_id):
    print("was it called")
    try:
        given_type = request.data["type"]
    except KeyError:
        out = {"status": 1, "message": "Type must be included in request"}
        return Response(out, status.HTTP_400_BAD_REQUEST)

    try:
        author = Author.objects.get(id=author_id)
    except Author.DoesNotExist:
        out = {"status": 1, "message": "Author not found"}
        return Response(out, status.HTTP_404_NOT_FOUND)

    try:
        inbox = Inbox.objects.get(author=author_id)
    except Inbox.DoesNotExist:
        out = {"status": 1, "message": "Author Inbox could not be found"}
        return Response(out, status.HTTP_404_NOT_FOUND)

    object_type = request.data["type"].lower()

    if object_type == "post":
        try:
            post_data = request.data
            # Add post to Inbox posts list
            if not inbox.posts:
                inbox.posts = [post_data]
            else:
                inbox.posts.append(post_data)

        except Exception as e:
            out = {"status": 1, "message": str(e)}
            return Response(out, status.HTTP_400_BAD_REQUEST)

    elif (
        object_type == "request"
        or object_type == "friend_request"
        or object_type == "follow"
    ):
        try:
            friend_request_data = request.data
            # Add friend request to Inbox requests list
            if not inbox.friend_requests:
                inbox.friend_requests = [friend_request_data]
            else:
                inbox.friend_requests.append(friend_request_data)

        except Exception as e:
            out = {"status": 1, "message": str(e)}
            return Response(out, status.HTTP_400_BAD_REQUEST)

    elif object_type == "comment":
        try:
            comment_data = request.data
            print("comment_data", comment_data)
            # Add comment to Inbox comments list
            if not inbox.comments:
                inbox.comments = [comment_data]
                print("Within inbox.comments 2", inbox.comments)
            else:
                inbox.comments.append(comment_data)
                print("Within inbox.comments", inbox.comments)

        except Exception as e:
            out = {"status": 1, "message": str(e)}
            return Response(out, status.HTTP_400_BAD_REQUEST)

    elif object_type == "like":
        try:
            like_data = request.data
            # Add like to Inbox likes list
            if not inbox.likes:
                inbox.likes = [like_data]
            else:
                inbox.likes.append(like_data)

        except Exception as e:
            out = {"status": 1, "message": str(e)}
            return Response(out, status.HTTP_400_BAD_REQUEST)

    else:
        out = {"status": 1, "message": "Type not allowed to be added to inbox"}
        return Response(out, status.HTTP_400_BAD_REQUEST)

    inbox.save()

    # Combine all items into a single list
    posts = inbox.posts if inbox.posts else []
    friend_requests = inbox.friend_requests if inbox.friend_requests else []
    likes = inbox.likes if inbox.likes else []
    comments = inbox.comments if inbox.comments else []

    items = posts + friend_requests + likes + comments

    out = {"type": "Inbox", "author": author_id, "items": items}
    return Response(out)


def clearInbox(request, author_id):
    try:
        author = Author.objects.get(id=author_id)  # specify for author
    except:
        out = {"status": 1, "message": "Author could not be found"}
        return Response(out, status.HTTP_404_NOT_FOUND)

    try:
        inbox = Inbox.objects.get(author=author_id)  # specify for author
    except:
        out = {"status": 1, "message": "Author Inbox could not be found"}
        return Response(out, status.HTTP_404_NOT_FOUND)

    # Clear posts
    inbox.posts.clear()

    # Clear friend requests
    inbox.friend_requests.clear()

    # Clear likes
    inbox.likes.clear()

    # Clear comments
    inbox.comments.clear()

    # save
    inbox.save()
    out = {"status": 0, "message": "Author's Inbox cleared"}
    return Response(out)


# inbox_endpoint
@swagger_auto_schema(
    method="get",
    operation_summary="Get all items in the author's inbox",
    responses={
        200: openapi.Response(description="List of items", schema=InboxSerializer),
    },
)
@swagger_auto_schema(
    method="post",
    operation_summary="Add an item to the author's inbox. MUST include origin field",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "type": openapi.Schema(type=openapi.TYPE_STRING),
            "origin": openapi.Schema(type=openapi.TYPE_STRING),
            # Add other required fields based on the type
        },
        required=["type", "origin"],
    ),
    responses={
        201: openapi.Response(
            description="Item added to inbox", schema=InboxSerializer
        ),
        400: openapi.Response(
            description="Bad request", schema=openapi.Schema(type=openapi.TYPE_OBJECT)
        ),
    },
)
@swagger_auto_schema(
    method="delete",
    operation_summary="Remove all items from the author's inbox",
    responses={
        200: openapi.Response(
            description="Inbox cleared", schema=openapi.Schema(type=openapi.TYPE_OBJECT)
        ),
    },
)
@api_view(allowed)
def inbox_endpoint(request, author_id):
    """
    get:
    get all posts sent to this author's inbox

    post:
    add a post, follow to this author's inbox. Need to include type for all objects.
    Need all relevant fields for all objects if adding new object. If sharing post, only need the post id and type.

    Example: adding follow:{
        "type": "Follow",
        "summary":"Greg wants to follow Lara",
        "actor":{
            "type":"author",
            "id":"http://127.0.0.1:5454/authors/1d698d25ff008f7538453c120f581471",
            "url":"http://127.0.0.1:5454/authors/1d698d25ff008f7538453c120f581471",
            "host":"http://127.0.0.1:5454/",
            "displayName":"Greg Johnson",
            "github": "http://github.com/gjohnson",
            "profileImage": "https://i.imgur.com/k7XVwpB.jpeg"
        },
        "object":{
            "type":"author",
            "id":"http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
            "host":"http://127.0.0.1:5454/",
            "displayName":"Lara Croft",
            "url":"http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
            "github": "http://github.com/laracroft",
            "profileImage": "https://i.imgur.com/k7XVwpB.jpeg"
        }
    }


    delete:
    remove all items from this author's inbox

    """

    author_id = toTrueIDAuthor(author_id)

    if request.method not in allowed:
        allowed_str = " ,".join(allowed)
        out = {"status": 1, "Allowed": allowed_str}
        return Response(out, status.HTTP_405_METHOD_NOT_ALLOWED)

    if request.method == "POST":
        return addItem(request, author_id)

    elif request.method == "GET":
        return getAll(request, author_id)

    elif request.method == "DELETE":
        return clearInbox(request, author_id)
