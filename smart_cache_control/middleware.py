# -*- coding: utf-8 -*-
import re
from datetime import datetime, timedelta

from django.conf import settings
import logging

# Getting variables from settings
try:
    VARY_HEADER = settings.SCC_SET_VARY_HEADER
except:
    VARY_HEADER = True

try:
    EXP_HEADER = settings.SCC_SET_EXPIRE_HEADER
except:
    EXP_HEADER = True

try:
    MAX_AGE_PUBLIC = settings.SCC_MAX_AGE_PUBLIC
except:
    MAX_AGE_PUBLIC = 86400

try:
    MAX_AGE_PRIVAT = settings.SCC_MAX_AGE_PRIVATE
except:
    MAX_AGE_PRIVAT = 0

try:
    CACHE_URLS = settings.SCC_CUSTOM_URL_CACHE
except:
    CACHE_URLS = []

logger = logging.getLogger(__name__)


class SmartCacheControlMiddleware(object):
    """
    Set the Cache-Control header automatically, defining not-authenticated
    requests as public (24h of cache by Default) and authenticated requests
    as private ( 0 seconds of cache ). This middleware class will also setup
    these HTTP headers:
        * Vary
        * Cache-Control
        * Expires

    You can customize a specific Cache-control value on each URL. For example
    if we want to avoid cache on /hello/ but always have it on /api/search we
    should write this in our settings file:

    SCC_CUSTOM_URL_CACHE = (
        (r'www\.example\.com/hello/$', 'private', 0),
        (r'www\.example2\.com/api/search$', 'public', 300),
    )

    Other options are available to customize the behaviour of the middleware:

    SCC_SET_VARY_HEADER: Define if the middleware have to set the Vary header.
                         Default value: True

    SCC_SET_EXPIRE_HEADER: Define if the middleware should set the Expires
                           header. Default value: True

    SCC_MAX_AGE_PUBLIC: Define the default max-age value in seconds for public
                        requests. Default value: 86400

    SCC_MAX_AGE_PRIVATE: Define the default max-age value in seconds for
                         private requests. Default value: 0

    """
    def process_response(self, request, response):
        meta = request.META.get('PATH_INFO', "")
        host = request.META.get('HTTP_HOST', "") + meta

        response['Cache-Control'] = 'public, max-age=%s' % MAX_AGE_PUBLIC
        expire_in = int(MAX_AGE_PUBLIC)

        if VARY_HEADER:
            response['Vary'] = 'User-Agent, Accept-Language, Cookie'

        try:
            if request.user.is_authenticated():
                expire_in = int(MAX_AGE_PRIVAT)
                response['Cache-Control'] = 'private, max-age={}'.format(
                    MAX_AGE_PRIVAT
                )

        except AttributeError:
            logger.warning(
                "smrtcc: Unable to determinate if the user is authenticated"
            )

        for url_pattern, cache_type, max_age, in CACHE_URLS:
            regex = re.compile(url_pattern)

            if regex.match(host):
                expire_in = max_age
                response['Cache-Control'] = '{type}, max-age={age}'.format(
                    type=cache_type,
                    age=max_age
                )

        if EXP_HEADER:
            expires = datetime.utcnow() + timedelta(seconds=expire_in)
            response['Expires'] = expires.strftime("%a, %d %b %Y %H:%M:%S GMT")

        return response
