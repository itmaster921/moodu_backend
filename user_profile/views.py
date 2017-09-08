import datetime

from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from rest_framework.renderers import JSONRenderer
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from user_profile.serializers import UserSerializer, GroupSerializer, UserProfileSerializer
from user_profile.models import UserProfile
from user_profile.SpotifyBackend import SpotifyBackend

from friendship.models import Follow


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class UserProfileViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows userprofiles to be viewed or edited.
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

@api_view(['POST'])
def create_user(request):
    """Creates a user in the database"""
    data = request.data
    user_obj = request.user
    user_obj.first_name = data.get('firstName')
    user_obj.last_name = data.get('lastName')
    user_obj.save()
    user_profile = user_obj.userprofile
    user_profile.email = data.get('email')
    birthday = datetime.datetime.strptime(data.get('birthday'), '%Y-%M-%d')
    user_profile.birthday = birthday
    user_profile.gender = data.get('gender')
    user_profile.location = data.get('location')
    user_profile = user_profile.save()
    # Serialize user and user profile.
    res = get_user_helper(user_obj)
    res.status = status.HTTP_201_CREATED
    return res

@api_view(['POST'])
def update_user(request):
    """Updates a user in the db"""
    data = request.data
    user_obj = request.user
    user_obj.first_name = data.get('firstName')
    user_obj.last_name = data.get('lastName')
    user_obj.save()
    user_profile = user_obj.userprofile
    user_profile.email = data.get('email')
    birthday = datetime.datetime.strptime(data.get('birthday'), '%Y-%m-%d')
    user_profile.birthday = birthday
    user_profile.gender = data.get('gender')
    user_profile.location = data.get('location')
    user_profile = user_profile.save()
    # Serialize user and user profile.
    return get_user_helper(user_obj)

def get_user_helper(user):
    """Returns information about a user so we can serialize it easily"""
    data = {}
    data['gender'] = user.userprofile.gender
    data['birthday'] = user.userprofile.birthday.strftime('%Y-%m-%d')
    data['spotify_id'] = user.userprofile.spotify_id
    data['location'] = user.userprofile.location
    data['first_name'] = user.first_name
    data['last_name'] = user.last_name
    data['email'] = user.email
    data['username'] = user.username
    try:
        data['profile_picture'] = user.userprofile.profile_picture.url
    except ValueError:
        data['profile_picture'] = ''
    try:
        data['profile_background_picture'] = user.userprofile.profile_background_picture.url
    except ValueError:
        data['profile_background_picture'] = ''
    data['followers'] = len(Follow.objects.followers(user))
    data['following'] = len(Follow.objects.following(user))
    return Response(data, status=status.HTTP_200_OK)

@api_view(['GET'])
def user(request, spotify_id):
    if request.method == 'GET':
        my_user = User.objects.get(userprofile__spotify_id=spotify_id)
        return get_user_helper(my_user)
    return Response({'error': 'Cannot find that user'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def user_autocomplete(request):
    """Very basic function that expects a 'q' url param and returns a list of users whose first name
    starts with whatever is in q.  This is case insensitive
    """
    query = request.GET.get('q')
    print "in user_autocomplete.  Query is: ", query
    if query:
        query_set = UserProfile.objects.filter(user__first_name__istartswith=query)
        # import pdb; pdb.set_trace()
        return Response(UserProfileSerializer(query_set, many=True, context={'request': request}).data, status=status.HTTP_200_OK)
    return Response({'error': 'Cannot find any users whose first name start with that query'},
                    status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def save_profile_picture(request):
    """Saves a user's profile picture"""
    if request.user:
        profile = request.user.userprofile
        picture = request.FILES['file']
        profile.profile_picture = picture
        profile.save()
        return Response(profile.profile_picture.url, status=status.HTTP_201_CREATED)
    return Response({'error': 'Cannot find that user'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def save_profile_background_picture(request):
    """Save's a user's profile background picture"""
    if request.user:
        profile = request.user.userprofile
        picture = request.FILES['file']
        profile.profile_background_picture = picture
        profile.save()
        return Response(profile.profile_background_picture.url, status=status.HTTP_201_CREATED)
    return Response({'error': 'Cannot find that user'}, status=status.HTTP_404_NOT_FOUND)