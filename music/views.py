import json

from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from models import Playlist, Song, Artist
from serializers import PlaylistSerializer

try:
    from django.contrib.auth import get_user_model
    user_model = get_user_model()
except ImportError:
    from django.contrib.auth.models import User
    user_model = User


# Create your views here.

@api_view(['POST', 'GET'])
def playlist(request):
    if request.method == 'GET':
        queryset = Playlist.objects.filter(user=request.user).order_by('-created_at')
        playlist_serializer = PlaylistSerializer(queryset, context={'request': request}, many=True)
        return Response(playlist_serializer.data, status=status.HTTP_200_OK)
    data = request.data
    user = request.user
    playlist_to_save = Playlist()
    playlist_to_save.title = data.get('title')
    playlist_to_save.message = data.get('message')
    playlist_to_save.locked = True if data.get('locked') == 'true' else False
    playlist_to_save.public = True if data.get('public') == 'true' else False
    playlist_to_save.latitude = data.get('latitude')
    playlist_to_save.longitude = data.get('longitude')
    playlist_to_save.user = user
    playlist_to_save.playlist_image = request.FILES.get('image')
    playlist_to_save.playlist_video = request.FILES.get('video')
    playlist_to_save.save()

    songs = data.get('songs', [])
    if type(songs) == type(""):
        songs = json.loads(songs)

    # Save songs
    for song_json in songs:
        images = song_json['album']['images']
        song, _ = Song.objects.get_or_create(
            title=song_json['name'],
            spotify_id=song_json['id'],
            spotify_uri=song_json['uri'],
            track_preview_url=song_json['preview_url'],
            album_artwork=images[0].get('url') if images else '',
            album_title=song_json['album']['name']
        )
        song.save()
        playlist_to_save.songs.add(song)

        for artist_json in song_json['artists']:
            artist, _ = Artist.objects.get_or_create(
                name=artist_json['name'],
                spotify_id=artist_json['id']
            )
            song.artists.add(artist)
    
    profiles = data.get('profiles', [])
    if type(profiles) == type(""):
        profiles = json.loads(profiles)
    
    for profile in profiles:
        share_with_user = get_object_or_404(user_model, username=profile['user']['username'])
        # user_id = profile_json['user']['id']
        playlist_to_save.shared_with_users.add(share_with_user)
    
    # notify_feed_of_playlist(user.userprofile, playlist_to_save)

    return Response(PlaylistSerializer(playlist_to_save,
                                       context={'request': request}).data,
                    status=status.HTTP_201_CREATED)
