from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings

try:
    from django.contrib.auth import get_user_model
    user_model = get_user_model()
except ImportError:
    from django.contrib.auth.models import User
    user_model = User

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from stream_django.feed_manager import feed_manager

from friendship.models import Friend, Follow, FriendshipRequest
from friendship.exceptions import AlreadyExistsError
from rest_friendship.serializers import FollowSerializer

get_friendship_context_object_name = lambda: getattr(settings, 'FRIENDSHIP_CONTEXT_OBJECT_NAME', 'user')
get_friendship_context_object_list_name = lambda: getattr(settings, 'FRIENDSHIP_CONTEXT_OBJECT_LIST_NAME', 'users')

@api_view(['GET'])
def followers(request, username):
    """ List this user's followers """
    user = get_object_or_404(user_model, username=username)
    the_followers = Follow.objects.followers(user)

    return Response(FollowSerializer(the_followers,
                                     context={'request': request}, many=True).data,
                    status=status.HTTP_200_OK)



@api_view(['GET'])
def following(request, username):
    """ List who this user follows """
    user = get_object_or_404(user_model, username=username)
    users_following = Follow.objects.following(user)

    return Response(FollowSerializer(users_following,
                                     context={'request': request}, many=True).data,
                    status=status.HTTP_200_OK)

@api_view(['GET'])
def follows(request, followee_username):
    """ returns whether or not the current user is following this person """
    user = get_object_or_404(user_model, username=followee_username)
    follows = Follow.objects.follows(request.user, user)

    return Response({'follows': follows},
                    status=status.HTTP_200_OK)


@api_view(['GET'])
def follow_counts(request, username):
    """ Gets counts for followers and followees """
    user = get_object_or_404(user_model, username=username)
    users_following = Follow.objects.following(user).count()
    users_followers = Follow.objects.followers(user).count()

    return Response({'following': users_following,
                     'followers': users_followers},
                    status=status.HTTP_200_OK)

@api_view(['POST'])
def follower_add(request, followee_username):
    """ Create a following relationship """

    print "IN FOLLOWER_ADD", followee_username
    exists = False
    if request.method == 'POST':
        followee = user_model.objects.get(username=followee_username)
        follower = request.user
        try:
            Follow.objects.add_follower(follower, followee)
            feed_manager.follow_user(follower.id, followee.id)
            exists = True
        except AlreadyExistsError:
            exists = True
        
        if exists:
            return Response({'result': 'success'},
                                status=status.HTTP_201_CREATED)
    return Response({'error': 'Invalid request'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def follower_remove(request, followee_username):
    """ Remove a following relationship """
    if request.method == 'POST':
        followee = user_model.objects.get(username=followee_username)
        follower = request.user
        Follow.objects.remove_follower(follower, followee)
        feed_manager.unfollow_user(follower.id, followee.id)
        return Response({'result': 'success'},
                        status=status.HTTP_200_OK)
    return Response({'error': 'Invalid request'}, status=status.HTTP_404_NOT_FOUND)