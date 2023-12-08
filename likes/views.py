from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Like
from .serializers import LikeSerializer

from app_posts.models import AppPost
from comments.models import Comment
from authors.models import Author

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

# Create your views here.

allowed = ['GET', 'POST']
allowed_id = ['GET']



baseURL_host = "node-net-46d70235bc29.herokuapp.com"
baseURL = f"https://{baseURL_host}/api"



def toTrueIDAuthor(author_id):
    return f"{baseURL}/authors/{author_id}"
def toTrueIDPost(author_id, post_id):
    return f"{baseURL}/authors/{author_id}/posts/{post_id}"
def toTrueIDComment(author_id, post_id, comment_id):
    return f"{baseURL}/authors/{author_id}/posts/{post_id}/comments/{comment_id}"
def toTrueIDPostLike(author_id, post_id, like_id):
    return f"{baseURL}/authors/{author_id}/posts/{post_id}/likes/{like_id}"
def toTrueIDCommentLike(author_id, post_id, comment_id, like_id):
    return f"{baseURL}/authors/{author_id}/posts/{post_id}/comments/{comment_id}/likes/{like_id}"

def getLikesPosts(request, author_id, post_id):
    likes = Like.objects.filter(object_on = post_id)
    try:
        serialiser = LikeSerializer(likes, many=True)
        out = {'status':0}
    
        like_list = []
        for like in serialiser.data:
            like_object = {}
            for field in like:
                like_object.update({field:like[field]})
            like_list.append(like_object)
        out.update({'data':like_list})
        print(out)
        return Response(out)
    
    except Exception as e:
        out = {'status':1,'message':str(e)}
        return Response(out, status.HTTP_400_BAD_REQUEST)


def getLikesComments(request, author_id, post_id, comment_id):
    likes = Like.objects.filter(object_on = comment_id)
    try:
        serialiser = LikeSerializer(likes, many=True)
        out = {'status':0}
    
        like_list = []
        for like in serialiser.data:
            like_object = {}
            for field in like:
                like_object.update({field:like[field]})
            like_list.append(like_object)
        out.update({'data':like_list})
        print(out)
        return Response(out)
    
    except Exception as e:
        out = {'status':1,'message':str(e)}
        return Response(out, status.HTTP_400_BAD_REQUEST)

def getLike(request, like_id):
    if len(like_id.split('/'))>1:
        like = Like.objects.get(pk=like_id)
    else:
        like = Like.objects.get(id2=like_id)

    try:
        try:
            serialiser = LikeSerializer(like)
            out = {'status':0, 'data':serialiser.data}
            return Response(out)
    
        except Exception as inner_e:
            out = {'status':1,'message':str(inner_e)}
            return Response(out, status.HTTP_400_BAD_REQUEST)

    except Exception as outer_e:
        out = {'status':2, 'message':str(outer_e)}
        return Response(out, status.HTTP_400_BAD_REQUEST)



def createLikePosts(request, author_id, post_id):
    """
    Create a new like for specified post on our website
    """
    try:
        #get the author who likes from the request
        author = Author.objects.get(id=request.data['author'])

        #get the summary from the request
        summary = "liked by " + author.username
        object_type = "post"
        object_on = post_id

        #create the new like
        if Like.objects.filter(author=author, object_on=object_on).exists():
            raise Exception("Like already exists")
        
        new_like = Like.objects.create(author=author, summary=summary, object_on=object_on, object_type = object_type)

        #updating the likes list on posts
        post = AppPost.objects.get(pk=post_id)
        post.liked.add(new_like)
        post.save()

        #serialise the new like
        serialiser = LikeSerializer(new_like)

        #return the new like
        out = {'status':0, 'data':serialiser.data}
        return Response(out, status.HTTP_201_CREATED)
    
    except Exception as e:
        out = {'status':1,'message':str(e)}
        return Response(out, status.HTTP_400_BAD_REQUEST)

def createLikeComments(request, author_id, post_id, comment_id):
    """
    Create a new like for specified post on our website
    """
    try:
        #get the author who likes from the request
        print("starting process of like creation")
        author = Author.objects.get(id=request.data['author'])

        #get the summary from the request
        summary = "liked by " + author.username
        object_type = "comment"

        object_on = comment_id

        #create the new like
        if Like.objects.filter(author=author, object_on=object_on).exists():
            raise Exception("Like already exists")
        
        print("creating new like object")
        new_like = Like.objects.create(author=author, summary=summary, object_on=object_on, object_type=object_type)
        print("new like object created")

        #updating the likes list on comments
        comment = Comment.objects.get(pk=comment_id)
        comment.liked.add(new_like)
        comment.save()

        #serialise the new like
        serialiser = LikeSerializer(new_like)

        #return the new like
        out = {'status':0, 'data':serialiser.data}
        return Response(out, status.HTTP_201_CREATED)
    
    except Exception as e:
        out = {'status':1,'message':str(e)}
        return Response(out, status.HTTP_400_BAD_REQUEST)



# likeComments
@swagger_auto_schema(
    method='get',
    operation_summary="Get all likes under a specific comment of a specific post",
    responses={
        200: openapi.Response(description="List of likes", schema=LikeSerializer),
    },
)
@swagger_auto_schema(
    method='post',
    operation_summary="Add a like under a specific comment of a specific post",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'author': openapi.Schema(type=openapi.TYPE_INTEGER),
        },
        required=['author'],
    ),
    responses={
        201: openapi.Response(description="New like added", schema=LikeSerializer),
        400: openapi.Response(description="Bad request", schema=openapi.Schema(type=openapi.TYPE_OBJECT)),
    },
)
@api_view(allowed)
def likeComments(request, author_id, post_id, comment_id):
    """
    GET: gets all likes under specific comment of specific post

    POST: add a like under specific comment of specific post. Requires the id of the author

    Example:{
        "author": 1
    }
    """
    comment_id = toTrueIDComment(author_id,post_id,comment_id)
    post_id = toTrueIDPost(author_id,post_id)
    author_id = toTrueIDAuthor(author_id)

    if request.method == 'GET':
        return getLikesComments(request, author_id, post_id, comment_id)
    
    elif request.method == 'POST':
        return createLikeComments(request, author_id, post_id, comment_id)


# likePosts
@swagger_auto_schema(
    method='get',
    operation_summary="Get all likes under a specific post",
    responses={
        200: openapi.Response(description="List of likes", schema=LikeSerializer),
    },
)
@swagger_auto_schema(
    method='post',
    operation_summary="Add a like under a specific post",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'author': openapi.Schema(type=openapi.TYPE_INTEGER),
        },
        required=['author'],
    ),
    responses={
        201: openapi.Response(description="New like added", schema=LikeSerializer),
        400: openapi.Response(description="Bad request", schema=openapi.Schema(type=openapi.TYPE_OBJECT)),
    },
)
@api_view(allowed)
@api_view(allowed)
def likePosts(request, author_id, post_id):
    """
    GET: gets all likes under specific post. Requires the id of the author

    POST: add a like under specific post

    Example:{
        "author": 1
    }
    """
    post_id = toTrueIDPost(author_id,post_id)
    author_id = toTrueIDAuthor(author_id)

    if request.method == 'GET':
        return getLikesPosts(request, author_id, post_id)
    
    elif request.method == 'POST':
        return createLikePosts(request, author_id, post_id)

# @api_view(allowed_id)
# def like_id(request, like_id):
#     """
#     Like a post
#     """
#     if request.method == 'GET':
#         return getLike(request, like_id)
    
    