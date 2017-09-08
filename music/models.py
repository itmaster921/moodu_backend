from django.conf import settings
from django.db import models

from stream_django.activity import Activity
from stream_django.feed_manager import feed_manager
from stream_django.activity import create_model_reference

class Artist(models.Model):
    """Stores information for a Spotify Artist"""
    name = models.CharField(max_length=200)
    spotify_id = models.TextField()

    def __str__(self):
        return self.name

class Song(models.Model):
    """Stores the information for a Spotify song that
    can be used in the creation of playlists, mood posts,
    or song prescriptions"""
    title = models.CharField(max_length=200)
    spotify_id = models.TextField()
    spotify_uri = models.TextField(default='')
    track_preview_url = models.URLField()
    album_artwork = models.URLField()
    album_title = models.TextField()
    artists = models.ManyToManyField(Artist)

    def __str__(self):
        return self.title

class Playlist(models.Model, Activity):
    """A collection of songs that can be shared with
     multiple users"""
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    title = models.TextField()
    message = models.TextField()
    locked = models.BooleanField()
    public = models.BooleanField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='creator')
    songs = models.ManyToManyField(Song)
    shared_with_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='shared_with')
    playlist_image = models.ImageField(upload_to='user_uploads', null=True)
    # Eventually change this to upload to a dir named after
    #  the user or something so it doesn't get too full.
    playlist_video = models.FileField(upload_to='video', null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)

    def __str__(self):
        return self.title

    @property
    def activity_object_serializer_class(self):
        from .serializers import PlaylistSerializer
        return PlaylistSerializer

    @property
    def activity_notify(self):
        """Notify everyone who the author has shared with"""
        feeds = [feed_manager.get_notification_feed(u.id) for u in self.shared_with_users.all()]
        return feeds
        
    @property
    def extra_activity_data(self):
        ref = create_model_reference(self.user.userprofile)
        return {'user_profile': ref }
