from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
import spotipy

# Create your views here.
def me(request):
    """ Returns json representing the user or None if the token is invalid 

    e.g. {u'product': u'open', u'display_name': u'Kelly Quinn Nicholes', u'external_urls': {u'spotify': u'https://open.spotify.com/user/22rtjcrjy7qe7lxwxzwpwpprq'}, u'country': u'US', u'uri': u'spotify:user:22rtjcrjy7qe7lxwxzwpwpprq', u'href': u'https://api.spotify.com/v1/users/22rtjcrjy7qe7lxwxzwpwpprq', u'followers': {u'total': 3, u'href': None}, u'images': [{u'url': u'https://scontent.xx.fbcdn.net/v/t1.0-1/p200x200/14141580_10153854114853008_298958832652656286_n.jpg?oh=f9122eb8da594fa69e642409ed2ac0a0&oe=5865CDA1', u'width': None, u'height': None}], u'type': u'user', u'id': u'22rtjcrjy7qe7lxwxzwpwpprq'}
    """
    access_token = request.GET.get('access_token')
    user = None
    sp = spotipy.Spotify(auth=access_token)
    try:
        user = sp.current_user()
        return JsonResponse(user)    
    except spotipy.client.SpotifyException:
        return JsonResponse({'error': 'Invalid access token'}, status=status.HTTP_403_FORBIDDEN)
        
    