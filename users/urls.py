from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from users import views

urlpatterns = [
    url(r'^login/', views.login),
    url(r'^search', views.search),
    url(r'^(?P<pk>\w{0,50})', views.UserView.as_view()),
    url(r'^', views.UserView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)