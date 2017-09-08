from __future__ import unicode_literals

from django.db import models
from django.conf import settings

MALE = 'M'
FEMALE = 'F'
GENDER_CHOICES = (
    (MALE, 'Male'),
    (FEMALE, 'Female')
)    

class UserProfile(models.Model):

    def __str__(self):
        return '%s %s' % (self.user.first_name, self.user.last_name)

    user = models.OneToOneField(settings.AUTH_USER_MODEL)     
    birthday = models.DateField(null=True)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=1, default=MALE, blank=True, null=True)
    spotify_id = models.CharField(max_length=40)
    location = models.CharField(max_length=200, blank=True, null=True)
    access_token = models.CharField(max_length=500, default='')
    refresh_token = models.CharField(max_length=500, default='')
    profile_picture = models.ImageField(upload_to='user_uploads', null=True)
    profile_background_picture = models.ImageField(upload_to='user_uploads', null=True)
