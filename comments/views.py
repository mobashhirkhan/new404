from django.shortcuts import render
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from app_posts.models import AppPost
from authors.models import Author

from .models import Comment
from .serialisers import CommentSerializer

# Create your views here.

# all accessible urls

allowed = ["GET", "POST"]
allowed_id = ["GET"]
types = ["plain", "markdown"]
# URL: ://service/authors/{AUTHOR_ID}/posts/{POST_ID}/comments


baseURL_host = "node-net-46d70235bc29.herokuapp.com"
baseURL = f"https://{baseURL_host}/api"


def toTrueIDAuthor(author_id):
    return f"{baseURL}/authors/{author_id}"
def toTrueIDPost(author_id, post_id):
    return f"{baseURL}/authors/{author_id}/posts/{post_id}"
def toTrueIDComment(author_id, post_id, comment_id):
    return f"{baseURL}/authors/{author_id}/posts/{post_id}/comments/{comment_id}"

def getComments(request, post_id):
    """
    Get the list of comments for speficied author for specified post on our website
    """
    comments = Comment.objects.filter(post=post_id)

    try:
        serialiser = CommentSerializer(comments, many=True)  # custom json parse error
        out = {"status": 0}

        comment_list = []
        for comment in serialiser.data:
            comment_object = {}
            for field in comment:
                comment_object.update({field: comment[field]})
            comment_list.append(comment_object)
        out.update({"comments": comment_list})
        return Response(out)

    except Exception as e:
        out = {"status": 1, "message": str(e)}
        return Response(out, status.HTTP_400_BAD_REQUEST)


def getComment(request, comment_id):
    """
    Get specific comment from list of comments for speficied author for specified post on our website
    """
    comment = Comment.objects.get(pk=comment_id)

    try:
        try:
            serialiser = CommentSerializer(comment)
            out = {
                "status": 0,
                "data": serialiser.data,
            }  # add the items in serialiser.data dict to out dict
            return Response(out)

        except Exception as inner_e:
            out = {"status": 1, "message": str(inner_e)}
            return Response(out, status.HTTP_400_BAD_REQUEST)

    except Exception as outer_e:
        out = {"status": 2, "message": str(outer_e)}
        return Response(out, status.HTTP_404_NOT_FOUND)


def addComment(request, author_id, post_id):
    """
    Add/Post new comment in list of comments under specified user under specified post
    """
    try:
        given_type = request.data["contentType"]
    except Exception as e:
        message = "Field 'contentType' is required. " + str(e)
        out = {"status": 1, "message": message}
        return Response(out, status=status.HTTP_400_BAD_REQUEST)

    # check if given type is valid
    if given_type not in types:
        message = "Invalid type. Valid choices are ‘plain’ and ‘markdown’."
        out = {"status": 1, "message": message}
        return Response(out, status=status.HTTP_400_BAD_REQUEST)

    # get serialised version of new comment
    try:
        post_author = Author.objects.get(id=author_id)
        post = AppPost.objects.get(pk=post_id)
        author = request.data["author"]
    except Exception as e:
        out = {"status": 1, "message": str(e)}
        return Response(out, status.HTTP_400_BAD_REQUEST)

    try:
        new_serialiser = CommentSerializer(data=request.data)
    except Exception as e:
        out = {"status": 1, "message": "json parse error" + str(e)}
        return Response(out, status.HTTP_400_BAD_REQUEST)

    # validate 1) serialixed, 2) id not included
    request_valid = new_serialiser.is_valid()
    id_not_included = "id" not in request.data

    # update db + show status
    if request_valid and id_not_included:
        new_serialiser.validated_data["post"] = post
        new_serialiser.save()  # save db'
        post.count += 1
        post.save()
        out = {
            "status": 0,
            "message": "New Comment added",
            "id": new_serialiser.data["id"],
        }
        print(new_serialiser.data)
        return Response(out)
    else:
        if not request_valid:  # If not valid, print errors
            errors = new_serialiser.errors
            print(errors)
            out = {"status": 1, "message": "Invalid request data", "errors": errors}
        elif not id_not_included:
            out = {
                "status": 1,
                "message": "Field 'id' cannot be included in comment information.",
            }
        else:
            out = {
                "status": 1,
                "message": "Comment could not be added. Review request body.",
            }
        return Response(out, status=status.HTTP_400_BAD_REQUEST)


# comment_endpoint
@swagger_auto_schema(
    method="post",
    operation_summary="Add a comment under a specified post of a specified author",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "author": openapi.Schema(type=openapi.TYPE_INTEGER),
            "contentType": openapi.Schema(type=openapi.TYPE_STRING),
            "content": openapi.Schema(type=openapi.TYPE_STRING),
        },
        required=["author", "contentType", "content"],
    ),
    responses={
        200: openapi.Response(
            description="New Comment added", schema=CommentSerializer
        ),
        400: openapi.Response(
            description="Invalid request data",
            schema=openapi.Schema(type=openapi.TYPE_OBJECT),
        ),
    },
)
@swagger_auto_schema(
    method="get",
    operation_summary="Get all comments under a specified post of a specified author",
    responses={
        200: openapi.Response(
            description="List of comments", schema=CommentSerializer(many=True)
        ),
    },
)

@api_view(allowed)
def comment_endpoint(request, author_id, post_id):
    """
    get:
    get all comments under a specified post of a specified author

    post:
    add a comment under a specified post of a specified author. Requires the author id of the commenter,
    the contentType(plain, markdown) and the content

    Example:{
            "author":7,
            "contentType":"plain",
            "content": "A comment by you"
    }

    """
    post_id = toTrueIDPost(author_id,post_id)
    author_id = toTrueIDAuthor(author_id)

    if request.method == "POST":
        return addComment(request, author_id, post_id)

    elif request.method == "GET":
        return getComments(request, post_id)

    else:
        allowed_str = " ,".join(allowed)
        out = {"status": 1, "Allowed": allowed_str}
        return Response(out, status.HTTP_405_METHOD_NOT_ALLOWED)


# comment_endpoint_id
@swagger_auto_schema(
    method="get",
    operation_summary="Get a specific comment under a specified post of a specified author",
    responses={
        200: openapi.Response(description="Comment details", schema=CommentSerializer),
    },
)
@api_view(allowed_id)
def comment_endpoint_id(request, author_id, post_id, comment_id):
    """
    get:
    get a specific comment under a specified post of a specified author

    """
    comment_id = toTrueIDComment(author_id,post_id,comment_id)

    if request.method == "GET":
        return getComment(request, comment_id)
    else:
        allowed_str = " ,".join(allowed_id)
        out = {"status": 1, "Allowed": allowed_str}
        return Response(out, status.HTTP_405_METHOD_NOT_ALLOWED)


"""
    author = Author.objects.get(pk=author_id)
    post = Post.objects.get(pk=post_id)
    
    try:
        author_serialiser = AuthorSerializer(author)
        post_serialiser = PostSerializer(post)
    except Exception as e:
        out = {'status':1,'message':str(e)}
        return Response(out, status.HTTP_400_BAD_REQUEST)
    
    comment_id = author_serialiser.data['host'] + author_serialiser.data['id'] + post_serialiser.data['id'] 
"""
