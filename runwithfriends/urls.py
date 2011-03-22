from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from runwithfriends.views import recent_runs, user_runs, run, realtime, refresh_user, logout


urlpatterns = patterns('',
    # Example:
    url(r"^$", recent_runs, name="recent_runs"),

    url(r"^user/(.*)/$", user_runs, name="user_runs"),
    url(r"^run/$", run, name="run"),
    url(r"^realtime/$", realtime, name="realtime"),
    url(r"^refresh-user/(.*)/$", refresh_user, name="refresh_user"),

    # our own logout, since social-auth doesn't have logout
    url(r"^logout/$", logout, name="logout"),

    # to be used with FB.init channel.html
    # see http://developers.facebook.com/docs/reference/javascript/FB.init/
    url(r"^channel.html$", direct_to_template, {'template': 'channel.html'}, name='channel_html'),

)
