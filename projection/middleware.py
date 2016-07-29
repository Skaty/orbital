import pytz

from django.utils import timezone


class TimezoneMiddleware(object):
    def process_request(self, request):
        if request.user and hasattr(request.user, 'preferences'):
            tzname = request.user.preferences.timezone
            timezone.activate(pytz.timezone(tzname))
        else:
            timezone.deactivate()