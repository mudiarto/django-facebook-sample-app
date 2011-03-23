# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.core.urlresolvers import reverse

from django.http import HttpResponseRedirect, Http404

from django.contrib import messages

import datetime
import base64
import cgi
from django.utils import simplejson as json

# support logout
from django.contrib.auth import logout as auth_logout

from runwithfriends.models import *

from django.contrib.auth.decorators import login_required #, permission_required

def htmlescape(text):
    """Escape text for use as HTML"""
    return cgi.escape(
        text, True).replace("'", '&#39;').encode('ascii', 'xmlcharrefreplace')




@csrf_exempt
def recent_runs ( request ):
    """
    if not logged in, will show the welcome screen
    if logged in, will show recent runs for the user and friends

    See the detail implementation. There are several combinations we have to handle:
        - user not logged in in regular website, doesn't give permission in facebook
            => that's fine, we still display the welcome screen
        - user not logged in in regular website, give permission in facebook
            => need to click on "login with facebook" button to create & associate account
        - user logged in with facebook in regular website, and access with the same facebook account
          in facebook app 
            => no problem , user can use it seamlessly
        - user logged in with email (or other) in regular website
            - accessing facebook with account that is not associated yet 
                => should offer to associate account
            - accessing facebook with account that is associated with different user id
                => should offer to logout and switch account


    
    """

    user = request.user

    if user.is_authenticated():
        user_recent_runs = user.runs.order_by('date')[:5]
        return render_to_response('runs.html',  {
            'user_recent_runs': user_recent_runs
            },
            context_instance=RequestContext(request))
    else:
        return render_to_response('welcome.html',  {
            },
            context_instance=RequestContext(request))

@login_required
def user_runs( request, user_id ):
    """Show a specific user's runs, ensure friendship with the logged in user"""
    # if self.user.friends.count(user_id) or self.user.user_id == user_id:
    if str(request.user.id) == user_id:
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            messages.add_message(request, messages.ERROR, 
                    "That user does not use Run with Friends.")
            return HttpResponseRedirect("/")
        runs = Run.objects.filter(user=user)

        return render_to_response('user.html',  {
            'user':user,
            'runs':runs,
            },
            context_instance=RequestContext(request))
    else:
        messages.add_message(request, messages.ERROR, 
                "You are not allowed to see that.")
        return HttpResponseRedirect("/")


class RunException(Exception):
    pass

@login_required
def run( request ):

    if request.method == "POST":
        try:
            location = request.POST[u'location'].strip()
            if not location:
                raise RunException(u'Please specify a location.')

            distance = float(request.POST[u'distance'].strip())
            if distance < 0:
                raise RunException(u'Invalid distance.')

            date_year = int(request.POST[u'date_year'].strip())
            date_month = int(request.POST[u'date_month'].strip())
            date_day = int(request.POST[u'date_day'].strip())
            if date_year < 0 or date_month < 0 or date_day < 0:
                raise RunException(u'Invalid date.')
            date = datetime.date(date_year, date_month, date_day)

            run = Run(
                user_id=request.user.id,
                location=location,
                distance=distance,
                date=date,
            )
            run.save()

            title = run.pretty_distance + u' miles @' + location
            publish = u'<a onclick=\'publishRun(' + \
                    json.dumps(htmlescape(title)) + u')\'>Post to facebook.</a>'

            messages.add_message(request, messages.SUCCESS,
                    "Successfully create project '%s' "%publish)
 
        except RunException, e:
            messages.add_message(request, messages.ERROR, e)
             #self.set_message(type=u'error', content=unicode(e))
        except KeyError:
            messages.add_message(request, messages.ERROR,
                    "Please specify location, distance & date.")
        except ValueError:
            messages.add_message(request, messages.ERROR,
                    "Please specify location, distance & date.")
        except Exception, e:
            messages.add_message(request, messages.ERROR,
                    "Unknown error occured. (%s)"%e)

    return HttpResponseRedirect("/")

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

