Wallabag
========

Service Description:
--------------------

a self hostable application for saving web pages

.. image:: https://raw.githubusercontent.com/foxmask/wallabag_api/master/wallabag.png

modifications of settings.py
----------------------------

1) INSTALLED_APPS :

.. code-block:: python

    INSTALLED_APPS = (
        'th_wallabag',
    )

2) Cache :

After the default cache add :

.. code-block:: python

    CACHES = {
        'default':
        {
            'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
            'LOCATION': BASE_DIR + '/cache/',
            'TIMEOUT': 600,
            'OPTIONS': {
                'MAX_ENTRIES': 1000
            }
        },
        # Wallabag Cache
        'th_wallabag':
        {
            'TIMEOUT': 500,
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": "redis://127.0.0.1:6379/9",
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            }
        },

3) TH_SERVICES

add this line to the TH_SERVICES setting

.. code-block:: python

    TH_SERVICES = (
        'th_wallabag.my_wallabag.ServiceWallabag',
    )

4) The service keys

Those will be required to be filled when activating the service for each user

Have a look at https://github.com/foxmask/wallabag_api/blob/master/README.rst for more details about them

creation of the table of the services
-------------------------------------

enter the following command

.. code-block:: bash

    python manage.py migrate


from the admin panel : activation of the service
------------------------------------------------

from http://yourdomain.com/admin/django_th/servicesactivated/add/


.. image:: https://raw.githubusercontent.com/foxmask/django-th/master/docs/admin_service_details.png


* Select "Wallabag",
* Set the Status to "Enabled"
* Check Auth Required: this will permit to redirect the user (or you) to your Wallabag application which will request a token
* Check Self Hosted: this will permit to enter the details about the service key we speak from point 4
* Fill a description

from "My Activated Service" page
--------------------------------

Now go to the page of "My Activated services" to enable it http://yourdomain.com/th/service/ by pressing the blue button
"Activate a new service"


.. image:: https://raw.githubusercontent.com/foxmask/django-th/master/docs/public_service_wallabag_add.png

then fill the fields that are required with the parameters, you got from point 4 earlier

.. image:: https://raw.githubusercontent.com/foxmask/django-th/master/docs/public_service_wallabag_settings.png

