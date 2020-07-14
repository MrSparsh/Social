from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from userapp import views

urlpatterns = [
    # url(r'^search', views.search),
    # url(r'^(?P<pk>\w{0,50})', views.UserView.as_view()),
    url(r'^$', views.index),
    url(r'^home/$', views.home),
    url(r'^all/$', views.users),
    url(r'^search/$', views.search),
    url(r'^set_password/$', views.set_password),
    url(r'^(?P<pk>\w{0,50})', views.userpage),
]

urlpatterns = format_suffix_patterns(urlpatterns)