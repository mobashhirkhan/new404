from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from app_posts.serializers import AppPostSerializer
import requests
from rest_framework import generics, pagination
from rest_framework.decorators import api_view, renderer_classes, authentication_classes, \
    permission_classes
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer

from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework import status
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from urllib.parse import urlparse

from likes.models import Like
from likes.serializers import LikeSerializer
from .models import Author
from .serializers import AuthorSerializer
from django.shortcuts import get_object_or_404, redirect, render

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

baseURL_host = "node-net-46d70235bc29.herokuapp.com"
baseURL = f"https://{baseURL_host}/api"


def toTrueID(author_id):
    return f"{baseURL}/authors/{author_id}"

@swagger_auto_schema(
    method="GET",
    operation_summary="List all Authors",
)
@api_view(["GET"])
@renderer_classes([BrowsableAPIRenderer, JSONRenderer])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def get_all_authors(request):
    """
    GET: Gets the list of all the authors

    """
    if request.method == "GET":
        query = Author.objects.all()

        page_number = request.GET.get('page')
        page_size = request.GET.get('size')

        if page_number and page_size:
            paginator = Paginator(query, page_size)
            try:
                query = paginator.get_page(page_number).object_list
            except PageNotAnInteger:
                query = paginator.get_page(1).object_list
            except EmptyPage:
                query = paginator.get_page(paginator.num_pages).object_list
        
        serializer = AuthorSerializer(query, many=True)

        return Response({"type": 'authors', "items": serializer.data})

@swagger_auto_schema(
    method="GET",
    operation_summary="Get author by ID",
    responses={
        200: openapi.Response(description="Successful operation", schema=AuthorSerializer),
        404: openapi.Response(description="Not Found"),
    }
)
@swagger_auto_schema(
    method="POST",
    operation_summary="Update author",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "displayName": openapi.Schema(type=openapi.TYPE_STRING),
            "github": openapi.Schema(type=openapi.TYPE_STRING),
            # Add other properties as needed
        },
        required=["displayName", "github"]  # Specify the required properties
    ),
    responses={
        200: openapi.Response(description="Successful operation", schema=AuthorSerializer),
        400: openapi.Response(description="Bad Request"),
        404: openapi.Response(description="Not Found"),
    }
)

@api_view(["GET", "POST"])
@renderer_classes([BrowsableAPIRenderer, JSONRenderer])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def get_author_by_id(request, author_id):
    """
    GET: Get author by id

    POST: Update author with specific id.

    Example:{
        "displayName": "NodeNetterExtreme"
        "github": ""
    }
    """
    author_id = toTrueID(author_id)
    try:
        author = Author.objects.get(id=author_id)
    except Author.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == "GET":
        serializer = AuthorSerializer(author)
        out = serializer.data
        return Response(out)
    
    elif request.method == "POST":
        serializer = AuthorSerializer(author, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            out = serializer.data
            return Response(out)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def get_github_activity(request, author_id):
    """ Get github activity """
    #author_id = request.data.get('author_id')

    author_id = toTrueID(author_id)
    author = Author.objects.get(id=author_id)
    parsed = urlparse(author.github)
    if not parsed.path:
        return render(request, 'base/github.html', {'error': 'No GitHub username found'}, status=404)
    github_username = parsed.path.split('/')[1]

    if github_username:
        response = requests.get(f'https://api.github.com/users/{github_username}/events')
        github_data = response.json()
        return render(request, 'base/github.html', {'github_data': github_data})
    else:
        return render(request, 'base/github.html', {'error': 'No GitHub username found'}, status=404)

####################################################################################
#FOLLOWS

@swagger_auto_schema(
    method='get',
    operation_summary="Get the list of author's followers",
    responses={
        200: openapi.Response(description="Successful operation", schema=AuthorSerializer),
        404: openapi.Response(description="Author not found"),
        405: openapi.Response(description="Method Not Allowed"),
    },
)
@api_view(["GET"])
@renderer_classes([BrowsableAPIRenderer, JSONRenderer])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def get_author_by_id_followers(request, author_id):
    """
    GET: Gets the list of all the author's followers(and true friends)
    """

    author_id = toTrueID(author_id)
    try:
        author = Author.objects.get(id=author_id)
    except Exception as e:
        out = {'status':1, 'message':str(e)}
        return Response(out, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        # Combine followers and friends into one
        followers = author.followers.all()
        friends = author.friends.all()
        foreign_authors = author.foreign_authors if author.foreign_authors else []
        items = list(followers) + list(friends) + foreign_authors

        serializer = AuthorSerializer(items, many=True)
        out = {'type':"followers", 'items': serializer.data}
        return Response(out)
    else:
        return Response(status.HTTP_405_METHOD_NOT_ALLOWED)


@swagger_auto_schema(
    method='get',
    operation_summary="Get the follower if they are a follower of the author",
    responses={
        200: openapi.Response(description="Successful operation", schema=AuthorSerializer),
        404: openapi.Response(description="Author or follower not found"),
    },
)
@swagger_auto_schema(
    method='put',
    operation_summary="Add an author to the list of author's followers",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "type": openapi.Schema(type=openapi.TYPE_STRING),
            "id": openapi.Schema(type=openapi.TYPE_STRING),
            "url": openapi.Schema(type=openapi.TYPE_STRING),
            "host": openapi.Schema(type=openapi.TYPE_STRING),
            "displayName": openapi.Schema(type=openapi.TYPE_STRING),
            "github": openapi.Schema(type=openapi.TYPE_STRING),
            # Add other properties as needed
        },
        required=['type', 'id', 'url', 'host', 'displayName']
    ),
    responses={
        200: openapi.Response(description="New follower added", schema=AuthorSerializer),
        404: openapi.Response(description="Author or follower not found"),
    },
)

@swagger_auto_schema(
    method='delete',
    operation_summary="Remove follower from the author's list of followers or true friends",
    responses={
        200: openapi.Response(description="Follower removed", schema=AuthorSerializer),
        404: openapi.Response(description="Author or follower not found"),
    },
)
@api_view(["GET","PUT","DELETE"])
@renderer_classes([BrowsableAPIRenderer, JSONRenderer])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def get_author_by_id_follower(request, author_id, foreign_id):
    """
    GET: Get follower is a follower or friend of author

    PUT: Add an author to list of authors. Only a username and pass is required. Can include other fields as well
    Example:{
            "type":"author",
            "id":"http://127.0.0.1:5454/authors/1d698d25ff008f7538453c120f581471",
            "url":"http://127.0.0.1:5454/authors/1d698d25ff008f7538453c120f581471",
            "host":"http://127.0.0.1:5454/",
            "displayName":"Greg Johnson",
            "github": "http://github.com/gjohnson",
        }
    DELETE: Remove follower from author's list of followers
    """

    author_id = toTrueID(author_id)
    try:
        author = Author.objects.get(id=author_id)
    except Exception as e:
        out = {'status':1, 'message':str(e)}
        return Response(out, status=status.HTTP_404_NOT_FOUND)

    if request.method == "PUT":
        try:
            data = request.data
            foreign_author = {
                "type": data["type"],
                "id": data["id"],
                "url": data["url"],
                "host": data["host"],
                "displayName": data["displayName"],
                "github": data["github"]
            }

            foreign_authors = author.foreign_authors if author.foreign_authors else []

            # Check if the new foreign author already exists in the list
            if foreign_author not in foreign_authors:
                # Add the new foreign author to the list
                foreign_authors.append(foreign_author)

                author.foreign_authors = foreign_authors
                author.save()

            # all in one
            followers = author.followers.all()
            friends = author.friends.all()
            items = list(followers) + list(friends) + foreign_authors

            serializer = AuthorSerializer(items, many=True)
            out = {'type': "followers", 'items': serializer.data}
            return Response(out)

        except Exception as e:
            out = {'status': 1, 'message': str(e)}
            return Response(out, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "GET":
        # get all types in one
        local_followers = author.followers.all()
        local_friends = author.friends.all()
        foreign_authors = author.foreign_authors if author.foreign_authors else []
        followers = list(local_followers) + list(local_friends) + foreign_authors

        try:
            follower = next(afollower for afollower in followers if afollower['id'] == foreign_id or afollower['url'].split('/')[-1] == foreign_id)
            follower_serializer = AuthorSerializer(follower)
            out = follower_serializer.data

        except StopIteration:
            out = {'status': 1, 'message': "Follower not found"}

        return Response(out)

    elif request.method == "DELETE":
        try:
            not_follower = None

            # Check if the foreign author is in the foreign_authors list
            foreign_authors = author.foreign_authors if author.foreign_authors else []
            for foreign_author in foreign_authors:
                if foreign_author['url'].split('/')[-1] == foreign_id:
                    not_follower = foreign_author
                    break

            if not_follower:
                # Remove the foreign author from the foreign_authors list
                foreign_authors.remove(not_follower)
                author.foreign_authors = foreign_authors
                author.save()

                out = {'status': 0, "removed_follower": not_follower}
                return Response(out)
            else:
                out = {'status': 1, 'message': 'Foreign author not found'}
                return Response(out, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            out = {'status': 1, 'message': str(e)}
            return Response(out, status=status.HTTP_400_BAD_REQUEST)

    else:
        return Response(status.HTTP_405_METHOD_NOT_ALLOWED)
###################################################################################################
#LIKED


@swagger_auto_schema(
    method='get',
    operation_summary="Get the list of liked objects by author",
    responses={
        200: openapi.Response(description="Successful operation", schema=LikeSerializer),
        404: openapi.Response(description="Author not found"),
    },
)
@api_view(["GET"])
@renderer_classes([BrowsableAPIRenderer, JSONRenderer])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def get_author_by_id_liked(request, author_id):
    """
    GET: all objects liked by author
    """
    author_id = toTrueID(author_id)
    if request.method == "GET":
        try:
            author = Author.objects.get(id=author_id)
        except Exception as e:
            out = {'status':1, 'message':str(e)}
            return Response(out, status=status.HTTP_404_NOT_FOUND)

        liked_objects = Like.objects.filter(author=author_id)
        try:
            like_serialiser = LikeSerializer(liked_objects, many=True) #custom json parse error
            out = {'status':0}

            liked = []
            for like in like_serialiser.data:
                liked_object = {}
                for field in like:
                    liked_object.update({field:like[field]})
                liked.append(liked_object)
            out.update({'liked':liked})
            return Response(out)

        except Exception as e:
            out = {'status':1,'message':str(e)}
            return Response(out, status.HTTP_400_BAD_REQUEST)


    else:
        return Response(status.HTTP_405_METHOD_NOT_ALLOWED)


