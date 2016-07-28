=====
Usage
=====

Activating services :
---------------------

The user activates the service for their own need. If the service requires an external authentication,
he will be redirected to the service which will ask him the authorization to acces the user's account.
Once it's done, goes back to django-trigger-happy to finish and record the "auth token".

Using the activated services :
------------------------------

a set of 3 pages will ask to the user information that will permit to trigger data from a service "provider" to a service "consumer".

For example :

* page 1 : the user gives a RSS feed
* page 2 : the user gives the name of the notebook where notes will be stored and a tag if he wants
* page 3 : the user gives a description


Fire the Triggers :
===================

Grabbing data and publishing data are done each 12min and 15min from your crontab
