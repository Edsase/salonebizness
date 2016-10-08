"""
Definition of urls for salonebizness.
"""

from django.conf.urls import include, url
from django.contrib import admin
from registration.backends.simple.views import RegistrationView #we want to modify the registration view of the registration app below

from news import views
from polls import views

#modify the registration view of the registration app using a wrapper
#the modification is to redirect the user to the index page if his registration is successful
class MyRegistrationView(RegistrationView):
    def get_success_url(self, user):
        return '/news/'
#to complete the modification, update the news/urls.py file by registering the registration view before the accounts registration

urlpatterns = [
    url(r'^admin/', admin.site.urls, name="admin"),
    #url(r"^$", views.index, name = "index"),
    #map url handling for the news app
    url(r'^news/', include('news.urls', namespace="news")),
    #map url for handling redirection of registration view
    url(r'^accounts/register/$', MyRegistrationView.as_view(), name = 'registration_register'),
    #map url handling for the registration app installed under pip
    url(r'^accounts/', include('registration.backends.simple.urls')),
    #map url handling for the polls app
    #url(r'^polls/', include('polls.urls')),
   
    
]























