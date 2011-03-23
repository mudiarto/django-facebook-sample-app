from django.conf import settings # import the settings file
from django.utils import simplejson as json
from django.core.urlresolvers import reverse
from socialregistration.models import FacebookProfile

def facebook(context):
    # return the value required by main.js
    user = context.user if context.user and context.user.is_authenticated() else None
    fb_profile = None

    if user:
        try:
            fb_profile = user.facebookprofile_set.get()
        except FacebookProfile.DoesNotExist:
            pass

    fbUserIdOnServer = fb_profile.uid if fb_profile else None

    js_conf = json.dumps({
            u'appId': settings.FACEBOOK_APP_ID,
            u'canvasName': settings.FACEBOOK_CANVAS_NAME,
            u'userIdOnServer': fbUserIdOnServer,
            u'channelUrl':reverse('channel_html'),
        })


    return {
            'js_conf': js_conf,
            'logged_in_user': user,
            'in_facebook':True if context.facebook_app else False,
    }
