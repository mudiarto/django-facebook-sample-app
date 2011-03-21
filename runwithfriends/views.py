# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.core.urlresolvers import reverse

from django.http import HttpResponseRedirect

# support logout
from django.contrib.auth import logout as auth_logout

@csrf_exempt
def recent_runs ( request ):
    """Show recent runs for the user and friends"""

    user = request.user

    if user.is_authenticated():
        return render_to_response('welcome.html',  {
            },
            context_instance=RequestContext(request))


        """
        friends = {}
        for friend in select_random(
                User.get_by_key_name(self.user.friends), 30):
            friends[friend.user_id] = friend

        self.render(u'runs',
            friends=friends,
            user_recent_runs=Run.find_by_user_ids(
                [self.user.user_id], limit=5),
            friends_runs=Run.find_by_user_ids(friends.keys()),
        )
        """
    else:
        return render_to_response('welcome.html',  {
            },
            context_instance=RequestContext(request))


def user_runs( request ):
    return render_to_response('welcome.html',  {
        },
        context_instance=RequestContext(request))

def run( request ):
    return render_to_response('welcome.html',  {
        },
        context_instance=RequestContext(request))

def realtime( request ):
    return render_to_response('welcome.html',  {
        },
        context_instance=RequestContext(request))

def refresh_user( request ):
    return render_to_response('welcome.html',  {
        },
        context_instance=RequestContext(request))


def logout(request):
    """
        implement our own logout since social-auth doesn't provide one
    """
    auth_logout(request)
    return HttpResponseRedirect(reverse('recent_runs'))

