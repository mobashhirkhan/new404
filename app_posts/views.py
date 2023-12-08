# Create your views here.
from rest_framework import generics

from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from authors.models import Author
# from .models import Author
from .models import AppPost
from .serializers import AppPostSerializer

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from django.shortcuts import get_object_or_404
from django.http import HttpResponse, Http404
import base64

#all accessible urls
#URL: ://service/authors/{AUTHOR_ID}/posts/{POST_ID}
#URL: ://service/authors/{AUTHOR_ID}/posts/
allowed = ['GET']
allowed_id = ['GET']
types = ["plain","markdown"]

baseURL_host = "node-net-46d70235bc29.herokuapp.com"
baseURL = f"https://{baseURL_host}/api"


def toTrueIDAuthor(author_id):
    return f"{baseURL}/authors/{author_id}"
def toTrueIDPost(author_id, post_id):
    return f"{baseURL}/authors/{author_id}/posts/{post_id}"
def getPosts(request, author_id):
    """
    Get the list of posts by specified author on our website
    """

    try:
        author = Author.objects.get(id=author_id) # specify for author
    except:
        out = {'status':1,'message':"Author could not be found"}
        return Response(out, status.HTTP_404_NOT_FOUND)

    posts = AppPost.objects.filter(author=author_id)
    
    try:
        serialiser = AppPostSerializer(posts, many=True) #custom json parse error
        # out = {'status': 0}
        
        post_list = []
        count = 0
        for post in serialiser.data:
            count += 1
            post_object = {}
            for field in post:
                post_object.update({field:post[field]})
            post_list.append(post_object)
        # out.update({'count':count,'data':post_list})
        out = {'items': post_list}
        return Response(out)
                
    except Exception as e:
        out = {'status': 1,'message': str(e)}
        return Response(out, status.HTTP_400_BAD_REQUEST)


def getPost(request, author_id, post_id):
    """
    Get specific post from list of posts by specific author on our website
    """

    try:
        author = Author.objects.get(id=author_id) # specify for author
    except:
        out = {'status':1,'message':"Author could not be found"}
        return Response(out, status.HTTP_404_NOT_FOUND)


    try:
        post = AppPost.objects.get(author=author_id, id=post_id)
    except Exception as e:
        print("GOT ERROR "+str(e))
        out = {'status':1,'message':"Post could not be found"}
        return Response(out, status.HTTP_404_NOT_FOUND)

    try:
        try:
            serialiser = AppPostSerializer(post)
            out = serialiser.data
            return Response(out)
        
        except Exception as inner_e:
            out = {'status':1,'message':str(inner_e)}
            return Response(out, status.HTTP_400_BAD_REQUEST)
        
    except Exception as outer_e:
        out = {'status':2, 'message':str(outer_e)}
        return Response(out, status.HTTP_404_NOT_FOUND)


def editPostPartial(request, author_id, post_id):
    """
    Edit post in list of posts under specified user.
    """

    hasType = 'contentType' in request.data
    if hasType: #can choose to edit contentType or not
        given_type = request.data['contentType']
        #check if given type is valid
        if given_type not in types:
            #bad request
            message = "Invalid type. Valid choices are ‘plain’ and ‘markdown’."
            out = {'status':1, 'message':message}
            return Response(out,status=status.HTTP_400_BAD_REQUEST)

    try:
        post = AppPost.objects.get(author=author_id,id=post_id)
    except:
        out = {'status':2, 'message':"Part could not be found"}
        return Response(out, status.HTTP_404_NOT_FOUND)

    try:
        if request.method=='POST':
            post_serialiser = AppPostSerializer(post, data=request.data, partial=True) #1 simple line, makes all the difference
        else:
            out = {'status':1}
            return Response(out, status.HTTP_405_METHOD_NOT_ALLOWED)

    except Exception as e:
        out = {'status':1,'message':str(e)}
        return Response(out, status.HTTP_400_BAD_REQUEST)

    #validate 1) serialixed, 2)id not included
    request_valid = post_serialiser.is_valid()
    id_not_included = 'id' not in request.data
    author_not_included = 'author' not in request.data

    if request_valid and id_not_included and author_not_included:
        post_serialiser.save()
        # out = {'status':0, 'message': "Post Edited"}
        out = post_serialiser.data
        return Response(out)

    else:
        if not id_not_included:
            out = {'status':1, 'message':"Field 'id' cannot be included in entry."}
        elif not author_not_included:
            out = {'status':1, 'message':"Field 'author' cannot be included in entry."}
        else:
            out = {'status':1, 'message':"Post could not be updated. Review request body. ", 'errors':post_serialiser.errors}
        return Response(out, status.HTTP_400_BAD_REQUEST)


def editPostFull(request, author_id, post_id):
    """
    Edit post in list of posts under specified user.
    """

    try:
        given_type = request.data['contentType']
    except Exception as e:
        message = "Field 'contentType' required. " + str(e)
        out = {'status':1, 'message':message}
        return Response(out,status=status.HTTP_400_BAD_REQUEST)

    hasType = 'contentType' in request.data
    if hasType: # can choose to edit contentType or not
        given_type = request.data['contentType']
        # check if given type is valid
        if given_type not in types:
            # bad request
            message = "Invalid type. Valid choices are ‘plain’ and ‘markdown’."
            out = {'status':1, 'message':message}
            return Response(out,status=status.HTTP_400_BAD_REQUEST)

    try:
        post = AppPost.objects.get(author=author_id,id=post_id)
    except:
        out = {'status':2, 'message':"Part could not be found"}
        return Response(out, status.HTTP_404_NOT_FOUND)
    
    try:
        if request.method=='PUT':
            post_serialiser = AppPostSerializer(post, data=request.data)
        else:
            out = {'status':1}
            return Response(out, status.HTTP_405_METHOD_NOT_ALLOWED)

    except Exception as e:
        out = {'status':1,'message':str(e)}
        return Response(out, status.HTTP_400_BAD_REQUEST)

    # validate 1)serialixed, 2)id not included
    request_valid = post_serialiser.is_valid()
    id_not_included = 'id' not in request.data
    author_not_included = 'author' not in request.data
    
    if request_valid and id_not_included and author_not_included:
        post_serialiser.save()
        # out = {'status':0, 'message': "Post Edited"}
        out = post_serialiser.data
        return Response(out)
        
    else:
        if not id_not_included:
            out = {'status':1, 'message':"Field 'id' cannot be included in entry."}
        elif not author_not_included:
            out = {'status':1, 'message':"Field 'author' cannot be included in entry."}
        else:
            out = {'status':1, 'message':"Post could not be updated. Review request body. ", 'errors':post_serialiser.errors}
        return Response(out, status.HTTP_400_BAD_REQUEST)


def removePost(request, author_id, post_id):
    """
    Remove a post from the post list of posts under specified user.
    """

    try:
        post = AppPost.objects.get(author=author_id,id=post_id)
    except:
        out = {'status':2, 'message':"Post could not be found"}
        return Response(out, status.HTTP_404_NOT_FOUND)

    post.delete()
    out = {'status':0, 'message':"Post removed"}
    return Response(out)

# getPosts
@swagger_auto_schema(
    method='get',
    operation_summary="Get the list of posts by specified author on our website",
    operation_id="get_posts",
    responses={
        200: openapi.Response(description="Successful operation", schema=AppPostSerializer(many=True)),
        404: openapi.Response(description="Author not found"),
    },
)
@api_view(allowed)
def post_endpoint(request, author_id):
    """
    get:
    get all posts of a specified author.

    """

    author_id = toTrueIDAuthor(author_id)

    if request.method not in allowed:
        allowed_str = " ,".join(allowed)
        out = {'status':1, 'Allowed':allowed_str}
        return Response(out, status.HTTP_405_METHOD_NOT_ALLOWED)

    elif request.method=='GET':
        return getPosts(request, author_id)

# getPost
@swagger_auto_schema(
    method='get',
    operation_summary="Get specific post from list of posts by specific author on our website",
    operation_id="get_post",
    responses={
        200: openapi.Response(description="Successful operation", schema=AppPostSerializer),
        404: openapi.Response(description="Author or Post not found"),
    },
)
@api_view(allowed_id)
def post_endpoint_id(request, author_id, post_id):
    """
    get:
    get a specific post of a specified author.

    """

    post_id = toTrueIDPost(author_id, post_id)
    author_id = toTrueIDAuthor(author_id)


    if request.method not in allowed_id:
        allowed_str = " ,".join(allowed_id)
        out = {'status':1, 'Allowed':allowed_str}
        return Response(out, status.HTTP_405_METHOD_NOT_ALLOWED)
        
    elif request.method=='GET':
        return getPost(request, author_id, post_id)
    elif request.method=='POST':
        return removePost(request,author_id, post_id)

        
def get_image_post(request, post_id, author_id):
    post = AppPost.objects.get(id=toTrueIDPost(author_id, post_id))
    if post.contentType == "image/png;base64" or post.contentType == "image/jpeg;base64":
        return HttpResponse(post.image, post.contentType)
    else:
        return HttpResponse({'Post is not an image'},status=status.HTTP_404_NOT_FOUND)