from django.conf import settings
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework import exceptions
from .models import UserProfile

import datetime
import json
import spotipy


class SpotifyBackend(BaseAuthentication):
    """
    Authenticate against the validity of the spotify user.
    """

    def authenticate_header(self, request):
        return 'Bearer'

    def authenticate(self, request):
        """Try to get the spotify user information from spotify.
        If the info comes back, get a user that has the same ID as the spotifyID.
        If it doesn't, return None.
        """
        print "in authenticate"
        spotify_auth_token = self.get_auth_token(request)
        sp = spotipy.Spotify(auth=spotify_auth_token)
        try:
            spotify_user = sp.current_user()
            print spotify_user
        except spotipy.client.SpotifyException, e:
            print "spotipy exception getting current user!", e.msg
            return None, None
        spotify_id = spotify_user['id']
        try:
            user_profile = UserProfile.objects.get(spotify_id=spotify_id)
            user = user_profile.user
        except UserProfile.DoesNotExist:
            display_name = spotify_user.get('display_name')
            first_name = ''
            last_name = ''
            if display_name != None and len(display_name) > 0:
                name_array = display_name.split(' ')
                print "getting first name from spotify"
                first_name = ' '.join(name_array[:-1])
                if len(name_array) > 0:
                    last_name = name_array[-1]
                    print "just got last name from spotify"
            user = User(username=spotify_id, 
                password=User.objects.make_random_password(), 
                email=spotify_user.get('email'),
                first_name=first_name,
                last_name=last_name
                )
            user.save()
            if spotify_user.get('birthdate'):
                birthday = datetime.datetime.strptime(spotify_user.get('birthdate'), '%Y-%M-%d')
            else:
                birthday = None
            gender = spotify_user.get('gender') if spotify_user.get('gender') else None
            location = spotify_user.get('location') if spotify_user.get('location') else None	
            user_profile = UserProfile(
                user=user,
                birthday = birthday,
                gender = gender,
                spotify_id = spotify_user.get('id'),
                location = location,
                access_token = spotify_auth_token
            )
            user_profile.save()
        return user, SpotifyBackend



    def get_user(self, user_id):
        try:
            return User.objects.get(username=user_id)
        except User.DoesNotExist:
            return None

    def get_auth_token(self, request):
        header = get_authorization_header(request)
        if not header:
            raise exceptions.AuthenticationFailed('No auth header.  Use Bearer')
        auth_header, token = header.split()
        if auth_header != 'Bearer':
            raise exceptions.AuthenticationFailed('Invalid auth header.  Use Bearer')
        if not token:
            raise exceptions.AuthenticationFailed('No token passed')
        return token
