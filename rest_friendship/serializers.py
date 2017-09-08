
from django.contrib.auth.models import User, Group
from rest_framework import serializers
from friendship.models import Follow

class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ('follower', 'followee', 'created')
