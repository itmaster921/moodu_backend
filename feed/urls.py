from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^user/(?P<username>\w{0,50})/', views.user, name="user"),
    url(r'^timeline/(?P<username>\w{0,50})/', views.timeline, name="timeline")
]