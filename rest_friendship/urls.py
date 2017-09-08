"""My own wrapper around django friendship to return DRF responses"""
try:
    from django.conf.urls import url
except ImportError:
    from django.conf.urls.defaults import url
from rest_friendship.views import  followers, follows, following, \
                                   follower_add, follower_remove, follow_counts

urlpatterns = [
    url(
        regex=r'^followers/(?P<username>[\w-]+)/$',
        view=followers,
        name='friendship_followers',
    ),
    url(
        regex=r'^following/(?P<username>[\w-]+)/$',
        view=following,
        name='friendship_following',
    ),
    url(
        regex=r'^follower/add/(?P<followee_username>[\w-]+)/$',
        view=follower_add,
        name='follower_add',
    ),
    url(
        regex=r'^follower/remove/(?P<followee_username>[\w-]+)/$',
        view=follower_remove,
        name='follower_remove',
    ),
    url(
        regex=r'^follower/follows/(?P<followee_username>[\w-]+)/$',
        view=follows,
        name='follows',
    ),
    url(
        regex=r'^counts/(?P<followee_username>[\w-]+)/$',
        view=follow_counts,
        name='follow_counts',
    ),
]
