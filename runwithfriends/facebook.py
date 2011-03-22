from django.conf import settings
from django.shortcuts import _get_queryset
from django.utils import simplejson as json

from social_auth.models import UserSocialAuth

import base64
import hmac
import hashlib
import time



class Facebook(object):
    """Wraps the Facebook specific logic"""
    def __init__(self, app_id=settings.FACEBOOK_APP_ID,
            app_secret=settings.FACEBOOK_API_SECRET):
        self.app_id = app_id
        self.app_secret = app_secret
        self.user_id = None
        self.access_token = None
        self.signed_request = {}

        # additional information for social_auth user
        self.social_auth = None # point to the UserSocialAuth associated with this facebook uid
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

class FacebookMiddleware(object):
    """
        check if it is a facebook canvas / page request
        It is facebook request if it is POST request, and contain valid signed-requests
    """
    def process_request(self, request):
        request.facebook = None

        if request.method == "POST":
            # if it contain signed request, then it may be from facebook
            facebook = Facebook()
            if facebook.load_signed_request(request.POST.get('signed_request')):
                # switch the request to GET, since this is actually a GET request
                request.method = "GET"
                request.facebook = facebook

                # check if the facebook user already associated with a django account
                # also set associated flag if the current (django) logged in user
                # is the same user as the associated facebook account
                # this is to handle the case where the webapp support different login mechanism
                # other than facebook.
                # e.g. user can be logged in to website with his email & password
                # but then go to facebook, and try to access our app with different facebook profile.
                # the middleware only detects this condition, it is up to the app to handle this case gracefully
                if facebook.is_authorized:
                    facebook.social_auth = get_object_or_None(UserSocialAuth,
                            provider='facebook', uid=facebook.user_id)
                    # check if both are the same user
                    if facebook.social_auth:
                        facebook.associated = (request.user == facebook.social_auth.user)

        return None

