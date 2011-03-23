from django.conf import settings
from django.shortcuts import _get_queryset
from django.utils import simplejson as json

from django.contrib import messages

from socialregistration.models import FacebookProfile

import base64
import hmac
import hashlib
import time


from django.contrib.auth import logout as auth_logout, login as auth_login

from runwithfriends.views import welcome_fb, associate

class FacebookApp(object):
    """
        Wraps the Facebook specific logic

        there are 3 flags we have to take care
        - is_authorized : whether facebook user give our app permission or not
        - profile : whether facebook user is already in our app or not
        - is_associated : whether current facebook user is the same as our django user
    """
    def __init__(self, app_id=settings.FACEBOOK_APP_ID,
            app_secret=settings.FACEBOOK_SECRET_KEY):
        self.app_id = app_id
        self.app_secret = app_secret
        self.user_id = None
        self.access_token = None
        self.signed_request = {}

        # additional information for social_auth user
        self.profile = None # point to the social registration's facebook profile associated with this facebook uid
        self.associated = False # true if associated with current request.user

    def load_signed_request(self, signed_request):
        """
            Load the user state from a signed_request value
            return true if it valid
        """
        valid = False
        if not signed_request:
            return valid

        try:
            sig, payload = signed_request.split(u'.', 1)
            sig = self.base64_url_decode(sig)
            data = json.loads(self.base64_url_decode(payload))

            expected_sig = hmac.new(
                self.app_secret, msg=payload, digestmod=hashlib.sha256).digest()

            # allow the signed_request to function for upto 1 day
            if sig == expected_sig and \
                    data[u'issued_at'] > (time.time() - 86400):
                self.signed_request = data
                self.user_id = data.get(u'user_id')
                self.access_token = data.get(u'oauth_token')
                valid = True
        except ValueError, ex:
            pass # ignore if can't split on dot

        return valid

    @property
    def is_authorized(self):
        return self.user_id is not None

    @property
    def is_associated(self):
        return self.associated

    @property
    def is_canvas_request(self):
        return self.user_id.get("page",None) is None

    @property
    def is_page_request(self):
        return self.user_id.get("page",None) is not None

    @staticmethod
    def base64_url_decode(data):
        data = data.encode(u'ascii')
        data += '=' * (4 - (len(data) % 4))
        return base64.urlsafe_b64decode(data)

    @staticmethod
    def base64_url_encode(data):
        return base64.urlsafe_b64encode(data).rstrip('=')


def get_object_or_None(klass, *args, **kwargs):
    queryset = _get_queryset(klass)
    try:
        return queryset.get(*args, **kwargs)
    except queryset.model.DoesNotExist:
        return None

class FacebookAppMiddleware(object):
    """
        check if it is a facebook canvas / page request
        It is facebook request if it is POST request, and contain valid signed-requests

    """
    def process_request(self, request):
        request.facebook_app = None

        if request.method == "POST":
            # if it contain signed request, then it may be from facebook
            facebook_app = FacebookApp()
            if facebook_app.load_signed_request(request.POST.get('signed_request')):
                # switch the request to GET, since this is actually a GET request
                request.method = "GET"
                request.facebook_app = facebook_app

                # handle if the facebook user already associated with a django account
                # also set associated flag if the current (django) logged in user
                # is the same user as the associated facebook account
                # this is to handle the case where the webapp support different login mechanism
                # other than facebook.
                # e.g. user can be logged in to website with his email & password
                # but then go to facebook, and try to access our app with different facebook profile.

                if facebook_app.is_authorized:
                    facebook_app.profile = get_object_or_None(FacebookProfile, uid=facebook_app.user_id)

                    # does user already have a facebook profile ?
                    if facebook_app.profile:
                        # yes, he does. Is it associated with current logged in user ?
                        # if yes, then good, do nothing
                        facebook_app.associated = (request.user == facebook_app.profile.user)

                        if request.user != facebook_app.profile.user:
                            # it is not associated, logged out the current  user, switch to fb user
                            if request.user.is_authenticated():
                                auth_logout(request)
                            # force login as facebook user
                            # NOTE: should we do it, or ask user first ?
                            new_user = facebook_app.profile.authenticate()
                            auth_login(request, new_user)
                            request.user = new_user
                            messages.success(request, "Login with Facebook")
                            facebook_app.associated = True
                # other cases will be handled by process_view

        return None

    def process_view(self, request, view_func, view_args, view_kwargs):
        """
        We may want to block request if we have inconsistent login.
        possible scenario :
        - user not logged in, doesn't have django fb account (offer to create new fb account)
        - user logged in via web, but doesn't have django fb account (offer to associate, or logout & create new account)
        - user logged in via web, already associated with different fb account (handled in process_response)
        """
        facebook_app  = request.facebook_app
        if not facebook_app:
            # not called from inside facebook
            return None

        if not facebook_app.is_authorized:
            # inside facebook, but we are not authorized yet
            return welcome_fb(request)

        if facebook_app.is_associated:
            # already logged in, and associated correctly, just continue
            return None

        # we are called inside facebook app, but with incorrect login - since user already logged in with
        # different credential
        user = request.user

        if user.is_authenticated() :
            # offer to associate his account
            return associate(request)
        else:
            # i wonder if it ever get here - authorized but not authenticated. 
            # maybe not, since it will be automatically handled by process_request
            # should always display welcome screen, offer to connect
            return welcome_fb(request)

