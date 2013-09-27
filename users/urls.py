from django.conf.urls import patterns, url
from users import views

urlpatterns = patterns('',
    url(r'^login/', views.loginuser, name='login'),
    url(r'^logout/', views.logoutuser, name='logout'),
    url(r'^register/', views.register, name='register'),
    url(r'^follow/(?P<followed_id>\d+)/$', views.follow_user, name='follow'),
    url(r'^(?P<user_id>\d+)/profile/$', views.profile, name='profile'),
)
