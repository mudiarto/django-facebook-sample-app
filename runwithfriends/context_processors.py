from django.conf import settings # import the settings file
from django.utils import simplejson as json
from django.core.urlresolvers import reverse

def facebook(context):
    # return the value required by main.js
    user = context.user if context.user and context.user.is_authenticated() else None
    user_id = user.id if user else None

    js_conf = json.dumps({
            u'appId': settings.FACEBOOK_APP_ID,
            u'canvasName': settings.FACEBOOK_CANVAS_NAME,
            u'userIdOnServer': user_id,
            u'channelUrl':reverse('channel_html')
        })


    return {
            'js_conf': js_conf,
            'logged_in_user': user,
    }
