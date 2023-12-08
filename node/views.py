from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404

from .models import Node
from .serializers import NodeSerializer
# Create your views here.

@api_view(['GET'])
def get_all_nodes(request):
    if request.method == 'GET':
        nodes = Node.objects.all()
        serializer = NodeSerializer(nodes, many=True)
        return Response({'type': 'nodes', 'nodes': serializer.data})

    # elif request.method == 'POST':
    #     serializer = NodeSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET','PUT','DELETE'])
# def get_node(request, id):
#     if request.method == 'GET':
#         node = get_object_or_404(Node, id=id)
#         serializer = NodeSerializer(node)
#         return Response({'type': 'Node', 'node': serializer.data})
#
#     elif request.method == 'PUT':
#         node = get_object_or_404(Node, id=id)
#         serializer = NodeSerializer(node, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     elif request.method == 'DELETE':
#         node = get_object_or_404(Node, id=id)
#         node.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
