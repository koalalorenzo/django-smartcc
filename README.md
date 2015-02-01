# django-smartcc
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

    # settings.py
    SCC_CUSTOM_URL_CACHE = (
        (r'/hello/$', 'private', 0),
        (r'/api/search$', 'public', 300),
    )

Other options are available to customize the behaviour of the middleware:

**SCC_SET_VARY_HEADER**: Define if the middleware have to set the Vary header.
                     Default value: *True*

**SCC_SET_EXPIRE_HEADER**: Define if the middleware should set the Expires
                       header. Default value: *True*

**SCC_MAX_AGE_PUBLIC**: Define the default max-age value in seconds for public
                    requests. Default value: *86400*

**SCC_MAX_AGE_PRIVATE**: Define the default max-age value in seconds for
                     private requests. Default value: *0*