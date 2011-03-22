# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.core.urlresolvers import reverse

from django.http import HttpResponseRedirect
import social_auth

# support logout
from django.contrib.auth import logout as auth_logout


@csrf_exempt
def recent_runs ( request ):
    """Show recent runs for the user and friends"""

    user = request.user

    # this value is set in facebook middleware
    facebook = request.facebook

    if facebook:
        # called from inside facebook
        if facebook.is_authorized and facebook.is_associated:
            # user already authorized & logged in
            # PROBLEM: it is possible that facebook authorize it, but we don't have
            # valid user (because user is not logged in to our application)
            # need to think also if user go to our site directly using login name "A"
            # but then also visit our site via facebook with different login name "B"
            # in that case, then i think facebook must have precedence,
            # but what happen if user go back to the original site using login name "A" ?
            # in that case, I think actually the best option is to stay with login "B" to allow
            # seamless integration between facebook & web app - like causes.com
            user_recent_runs = user.runs.order_by('date')[:5]
            return render_to_response('runs.html',  {
                'user_recent_runs': user_recent_runs
                },
                context_instance=RequestContext(request))
        else:
            # called from facebook, but user doesn't give permission yet
            # i think the best action here is to ask very basic permission from user
            # we can't redirect view, so we have to call the function directly
            return render_to_response('welcome.html',  {
                },
                context_instance=RequestContext(request))
    else:
        # called directly
        if user.is_authenticated():
            return render_to_response('welcome.html',  {
                },
                context_instance=RequestContext(request))
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

