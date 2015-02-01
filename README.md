# django-smartcc
Set some cache-related headers automatically, defining not-authenticated
requests as public and authenticated requests as private. You can also customize these values for specific URLs. This middleware class will also setup these HTTP headers:

* Vary
* Cache-Control
* Expires

## Installation
Add django-smartcc on your requirements.txt file or just launch:

    pip install -U django-smartcc
   
Then add django-smartcc in the installed apps and in the middleware, so add these line in your settings.py file.

    # settings.py
    INSTALLED_APPS += [
        'smart_cache_control',    ]
    
    MIDDLEWARE_CLASSES += [
        'smart_cache_control.middleware.SmartCacheControlMiddleware'
    ]

**Note**: Remember that this middleware requires authentication, so it should be loaded after the *django.contrib.auth.middleware.AuthenticationMiddleware*!
    

## Customization and Settings
You can customize a specific Cache-control value on each URL. For example
if we want to avoid cache on */hello/* , but always have it on */api/search* for 5 minutes, we should write this in our settings file:

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