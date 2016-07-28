===================
Create a new module
===================

2 ways to reach the goal to "bootstrap" a new TriggerHappy module :

1 - django-th-ansible :
=======================

just simple and fast ;)

with git, clone [django-th-ansible](https://github.com/foxmask/django-th-ansible), modify the site.yml file and run:


.. code-block:: python

   ansible-playbook -i site.yml


Now aour new module is ready to be customized for your new service (template, models and so on).


2 - django-th-dummy :
=====================

Introduction :
--------------

You can start a new module by cloning the project `Django Th Dummy <https://github.com/foxmask/django-th-dummy>`_
which is a vanilla django module, ready to be used, after you've replaced the name of the form/model/class we'll see below

Once you've cloned it, rename the folder th_dummy to the name of your choice.

Below we'll keep the name dummy to continue our explanation


Forms :
-------

the form **th_dummy/forms.py** provides 3 forms :

* **DummyForm** a modelForm
* **DummyFormProvider** which extends DummyForm
* **DummyFormConsumer** which extends DummyForm


DummyForm will define the content of our form, our fields our widget etc


Models :
--------

the model **th_dummy/models.py** :

.. code-block:: python

    class Dummy(Services):

        # put whatever you need  here
        # eg title = models.CharField(max_length=80)
        # but keep at least this one
        title = models.CharField(max_length=80)
        trigger = models.ForeignKey('TriggerService')

        class Meta:
            app_label = 'django_th'

        def __str__(self):
            return "%s" % (self.name)

        def show(self):
            return "My Dummy %s" % (self.name)


Key points :
~~~~~~~~~~~~

* The model is related to TriggerService model
* The model uses the **app_label** to **django_th** meta, so the Trigger Happy will be added the table name


Service class :
---------------

at the beginning of the class **ServiceDummy** (from `th_dummy/my_dummy.py`) you will need to import the class of the
third party application

the class `ServiceDummy` will extend `ServiceMgr` we've imported from `django_th.services.services`

This class is composed at least by 2 methods :


save_data :
~~~~~~~~~~~


we provider the following parms

* token - the token of the service
* trigger_id - the trigger id we handle,
* data - the data to store (title, url, content), provided by a "process_data" of another service

role : save the data to the `ServiceDummy`

return : a boolean True or False, if the save_data worked fine or not

If the service does not save data, it's the case of the module django-th-rss which just provides stuff and save nothing,
you'll put `pass` to save_data as the body of your code

auth and callback :
~~~~~~~~~~~~~~~~~~~

If your service need an authentication, you'll need 2 new functions `auth` and `callback`

* `auth` will trigger the authentication to the third party application, the Oauth process in fact
* `callback` is triggered when the authentication is done and call by the third party application.
At this step the callback function store the oauth token to the dedicated dummy model


The complete code of this class :
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


.. code-block:: python

    # coding: utf-8
    # add here the call of any native lib of python like datetime etc.
    #
    # add the python API here if needed
    from external_api import CallOfApi

    # django classes
    from django.conf import settings
    from django.utils.log import getLogger

    # django_th classes
    from django_th.services.services import ServicesMgr
    from django_th.models import UserService, ServicesActivated

    """
        handle process with dummy
        put the following in settings.py

        TH_DUMMY = {
            'consumer_key': 'abcdefghijklmnopqrstuvwxyz',
        }

        TH_SERVICES = (
            ...
            'th_dummy.my_dummy.ServiceDummy',
            ...
        )

    """

    logger = getLogger('django_th.trigger_happy')


    class ServiceDummy(ServicesMgr):


        def __init__(self, ):
            self.dummy_instance = external_api.CallOfApi(
                    settings.TH_DUMMY['consumer_key'], token)

        def read_data(self, token, trigger_id, date_triggered):
            """
                get the data from the service
                :param trigger_id: trigger ID to process
                :param date_triggered: the date of the last trigger
                :type trigger_id: int
                :type date_triggered: datetime
                :return: list of data found from the date_triggered filter
                :rtype: list
            """
            data = list()
            return cache.set('th_dummy_' + str(trigger_id), data)

        def save_data(self, token, trigger_id, **data):
            """
                let's save the data

                :param trigger_id: trigger ID from which to save data
                :param **data: the data to check to be used and save
                :type trigger_id: int
                :type **data:  dict
                :return: the status of the save statement
                :rtype: boolean
            """
            from th_dummy.models import Dummy
            status = False

            if token and data.get('link'):
                # get the data of this trigger
                trigger = Dummy.objects.get(trigger_id=trigger_id)
                # if the external service need we provide
                # our stored token and token secret then I do
                # token_key, token_secret = token.split('#TH#')

                title = ''
                title = (data.get('title') if data.get('title') else '')
                    # add data to the external service
                item_id = self.dummy_instance.add(
                    url=data['link'], title=title, tags=(trigger.tag.lower()))

                sentance = str('dummy {} created').format(data.get('link'))
                logger.debug(sentance)
                status = True
            else:
                logger.critical(
                    "no token or link provided for trigger ID {} ".format(trigger_id))
                status = False
            return status

        def auth(self, request):
            """
                let's auth the user to the Service
            """
            request_token = super(ServiceDummy, self).auth(request)
            callback_url = self.callback_url(request, 'dummy')

            # URL to redirect user to, to authorize your app
            auth_url_str = '%s?oauth_token=%s&oauth_callback=%s'
            auth_url = auth_url_str % (self.AUTH_URL,
                                       request_token['oauth_token'],
                                       callback_url)

            return auth_url

        def callback(self, request):
            """
                Called from the Service when the user accept to activate it
            """
            kwargs = {'access_token': '', 'service': 'ServiceDummy',
                      'return': 'dummy'}
            return super(ServiceDummy, self).callback(request, **kwargs)
