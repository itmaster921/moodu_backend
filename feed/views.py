from django.shortcuts import render

try:
    from django.contrib.auth import get_user_model
    user_model = get_user_model()
except ImportError:
    from django.contrib.auth.models import User
    user_model = User
    
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from user_profile.serializers import UserSerializer, UserProfileSerializer
from user_profile.models import UserProfile
from stream_django.feed_manager import feed_manager
from stream_django.enrich import Enrich


enricher = Enrich()


# Create your views here.
@api_view(['GET'])
def user(request, username):
    """Returns the user feed from getstream"""
    print "USERNAME FOR USER FEED: %s" % username
    user_obj = user_model.objects.get(username=username)
    user_feed = feed_manager.get_user_feed(user_obj.id)
    activities = user_feed.get(limit=25)['results']
    enriched_activities = enricher.enrich_activities(activities)
    serialized_activities = serialize_activities(enriched_activities, request)
    return Response(serialized_activities, status=status.HTTP_200_OK)

@api_view(['GET'])
def timeline(request, username):
    """Returns the timeline from getstream"""
    print "USERNAME FOR TIMELINE FEED: %s" % username
    user_obj = user_model.objects.get(username=username)
    timeline_feed = feed_manager.get_news_feeds(user_obj.id)['timeline']
    activities = timeline_feed.get(limit=25)['results']
    enriched_activities = enricher.enrich_activities(activities)
    serialized_activities = serialize_activities(enriched_activities, request)
    return Response(serialized_activities, status=status.HTTP_200_OK)

def get_serialized_object_or_str(obj):
    """Grabs from the model the field to determine what class to serialize"""
    if hasattr(obj, 'activity_object_serializer_class'):
        obj = obj.activity_object_serializer_class(obj).data
    else:
        obj = str(obj)  # Could also raise exception here
    return obj

def serialize_activities(activities, request):
    """Serializes the objects based on a property "activity_object_serializer_class"""
    for activity in activities:
        activity['object'] = get_serialized_object_or_str(activity['object'])
        user = activity['actor']
        activity['actor'] = UserSerializer(activity['actor'], context={'request': request}).data
        user_profile = UserProfile.objects.get(user=user)
        activity['profile'] = UserProfileSerializer(user_profile).data
    return activities
