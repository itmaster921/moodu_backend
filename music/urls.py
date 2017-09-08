from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^playlist/', views.playlist, name="playlist")
]