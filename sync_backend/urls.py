"""sync_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import url, include
from rest_framework import routers
from user_profile import views as user_profile_views
from spotify import views as spotify_views
from django.conf import settings
from django.conf.urls.static import static



router = routers.DefaultRouter()
router.register(r'users', user_profile_views.UserViewSet)
router.register(r'groups', user_profile_views.GroupViewSet)
router.register(r'user_profile', user_profile_views.UserProfileViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/spotify/me', spotify_views.me, name='me'),
    url(r'^api/user/create', user_profile_views.create_user, name='create_user'),
    url(r'^api/user/update', user_profile_views.update_user, name='update_user'),
    url(r'^api/user/autocomplete', user_profile_views.user_autocomplete, name='user_autocomplete'),
    url(r'^api/user/(?P<spotify_id>\w{0,50})', user_profile_views.user, name='user'),
    url(r'^api/profile-picture', user_profile_views.save_profile_picture, name='save_profile_picture'),
    url(r'^api/profile-background-picture', user_profile_views.save_profile_background_picture, name='save_profile_background_picture'),
    url(r'^api/music/', include('music.urls')),
    url(r'^api/feed/', include('feed.urls')),
    url(r'^api/friendship/', include('rest_friendship.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
