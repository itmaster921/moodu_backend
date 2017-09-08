from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Playlist, Song, Artist
from user_profile.serializers import UserSerializer, UserProfileSerializer


class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ('name', 'spotify_id')

class SongSerializer(serializers.ModelSerializer):
    artists = ArtistSerializer(many=True, read_only=True)
    class Meta:
        model = Song
        fields = ('title', 'spotify_id', 'spotify_uri', 'track_preview_url', 'album_artwork', 'album_title', 'artists')

class PlaylistSerializer(serializers.ModelSerializer):
    songs = SongSerializer(many=True, read_only=True)
    shared_with_users = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Playlist
        fields = ('created_at', 'modified_at', 'title', 'message', 'locked', 'public', 'user', 'songs', 'shared_with_users', 'playlist_image', 'playlist_video', 'latitude', 'longitude')




