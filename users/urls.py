from django.conf.urls import patterns, url
from users import views

urlpatterns = patterns('',
    url(r'^register/', views.register, name='register'),
    url(r'^save/', views.save, name='save'),
)