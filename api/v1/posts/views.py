from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny , IsAuthenticated
from rest_framework.response import Response
from api.v1.main.functions import generate_serializer_errors
from django.shortcuts import get_object_or_404
from posts.models import Post , Comment
from api.v1.posts.serializers import *
from rest_framework import status
from accounts.models import *

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def posts(request):
    if Post.objects.filter(is_deleted=False).exists():
        posts = Post.objects.filter(is_deleted=False)

        serialized_data = PostSerializer(instance=posts,context = {"request": request},many=True).data

        response_data = {
            "StatusCode": 6000,
            "data" : serialized_data   
        }
    else:
        response_data = {
            "StatusCode": 6001,
            "data" : {
                "title" : "failed",
                "message" : "Currently, there are no Posts available"
            }
        }

    return Response(response_data, status=status.HTTP_200_OK)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def post(request,pk):
    if Post.objects.filter(is_deleted=False, id=pk).exists():
        posts = Post.objects.get(is_deleted=False, id=pk)

        serialized_data = PostSerializer(instance=posts,context = {"request": request}).data

        response_data = {
            "StatusCode": 6000,
            "data" : serialized_data   
        }
    else:
        response_data = {
            "StatusCode": 6001,
            "data" : {
                "title" : "failed",
                "message" : "This post is not avaliable at this moment"
            }
        }

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_post(request):
    serializer = CreatePostSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save() 
        
        response_data = {
            'StatusCode': 6000,
            'data': {
                'title': 'Success!',
                'message': 'Post added successfully',
            }
        }
    else:
        response_data = {
            "StatusCode": 6001,
            "data": {
                "title": "Failed",
                "errors": generate_serializer_errors(serializer.errors),
            }
        }
    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_post(request):
    user_profile = request.user.userprofile

    if Post.objects.filter(is_deleted=False, user=user_profile).exists():
        posts = Post.objects.filter(is_deleted=False,  user=user_profile)

        serialized_data = PostSerializer(posts,context = {"request": request},many=True).data

        response_data = {
            "StatusCode": 6000,
            "data" : serialized_data   
        }
    else:
        response_data = {
            "StatusCode": 6001,
            "data" : {
                "title" : "failed",
                "message" : "This post is not avaliable at this moment"
            }
        }

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def comments(request,pk):
    if Comment.objects.filter(is_deleted=False,post__id=pk).exists():
        comment = Comment.objects.filter(is_deleted=False,post__id=pk)

        serialized_data = CommentSerializer(comment,context = {"request": request},many=True).data

        response_data = {
            "StatusCode": 6000,
            "data" : serialized_data   
        }
    else:
        response_data = {
            "StatusCode": 6001,
            "data" : {
                "title" : "failed",
                "message" : "Currently, there are no Comments available"
            }
        }

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_comment(request, pk):
    user_profile = request.user.userprofile  

    serializer = AddCommentSerializer(data=request.data)
    if serializer.is_valid():
            post = Post.objects.get(id=pk)
            serializer.save(user=user_profile, post=post)

            response_data = {
                "StatusCode": 6000,
                "data": {
                    "title": "Success",
                    "message": "Comment added successfully"
                }
            }
    else:
        response_data = {
            "StatusCode": 6001,
            "data": {
                "title": "Failed",
                "errors": serializer.errors
            }
        }
    return Response(response_data, status=status.HTTP_200_OK)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def toggle_like_post(request, pk):
    user_profile = request.user.userprofile  

    if Post.objects.filter(id=pk).exists():
        post = Post.objects.get(id=pk)

        if user_profile in post.like.all():
            post.like.remove(user_profile)  
            action = "unliked"
        else:
            post.like.add(user_profile)
            action = "liked"

        response_data = {
            "StatusCode": 6000,
            "data": {
                "title": "Success",
                "message": f"Post successfully {action}",
            },
        }
    else:
        response_data = {
            "StatusCode": 6001,
            "data": {
                "title": "Failed",
                "message": "Post not found",
            },
        }
    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def schools(request):
    if School.objects.filter(is_deleted=False).exists():
        school = School.objects.filter(is_deleted=False)

        serialized_data = SchoolSerializer(instance=school,context = {"request": request},many=True).data

        response_data = {
            "StatusCode": 6000,
            "data" : serialized_data   
        }
    else:
        response_data = {
            "StatusCode": 6001,
            "data" : {
                "title" : "failed",
                "message" : "Currently, there are no Posts available"
            }
        }

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def users_post(request,pk):

    if Post.objects.filter(is_deleted=False, user__id=pk).exists():
        posts = Post.objects.filter(is_deleted=False,  user__id=pk)

        serialized_data = PostSerializer(posts,context = {"request": request},many=True).data

        response_data = {
            "StatusCode": 6000,
            "data" : serialized_data   
        }
    else:
        response_data = {
            "StatusCode": 6001,
            "data" : {
                "title" : "failed",
                "message" : "This post is not avaliable at this moment"
            }
        }

    return Response(response_data, status=status.HTTP_200_OK)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def toggle_saved(request, pk):
    user_profile = request.user.userprofile  

    if Post.objects.filter(id=pk).exists():
        post = Post.objects.get(id=pk)

        if user_profile in post.saved_by.all():
            post.saved_by.remove(user_profile)  
            action = "unsaved"
        else:
            post.saved_by.add(user_profile)
            action = "saved"

        response_data = {
            "StatusCode": 6000,
            "data": {
                "title": "Success",
                "message": f"Post successfully {action}",
            },
        }
    else:
        response_data = {
            "StatusCode": 6001,
            "data": {
                "title": "Failed",
                "message": "Post not found",
            },
        }
    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def saved_posts(request):
    user_profile = request.user.userprofile  

    if Post.objects.filter(is_deleted=False,  saved_by=user_profile).exists():
        posts = Post.objects.filter(is_deleted=False,  saved_by=user_profile)

        serialized_data = SavedSerializer(posts,context = {"request": request},many=True).data

        response_data = {
            "StatusCode": 6000,
            "data" : serialized_data   
        }
    else:
        response_data = {
            "StatusCode": 6001,
            "data" : {
                "title" : "failed",
                "message" : "This post is not avaliable at this moment"
            }
        }

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def saved_posts_bt_users(request,pk):

    if Post.objects.filter(is_deleted=False,  saved_by=pk).exists():
        posts = Post.objects.filter(is_deleted=False,  saved_by=pk)

        serialized_data = SavedSerializer(posts,context = {"request": request},many=True).data

        response_data = {
            "StatusCode": 6000,
            "data" : serialized_data   
        }
    else:
        response_data = {
            "StatusCode": 6001,
            "data" : {
                "title" : "failed",
                "message" : "This post is not avaliable at this moment"
            }
        }

    return Response(response_data, status=status.HTTP_200_OK)
