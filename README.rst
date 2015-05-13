ecommerce  |Travis|_ |Coveralls|_
=================================
.. |Travis| image:: https://travis-ci.org/edx/ecommerce.svg?branch=master
.. _Travis: https://travis-ci.org/edx/ecommerce

.. |Coveralls| image:: https://coveralls.io/repos/edx/ecommerce/badge.svg?branch=master
.. _Coveralls: https://coveralls.io/r/edx/ecommerce?branch=master

Overview
--------

This repository contains the edX ecommerce service, which relies heavily on `django-oscar <https://github.com/edx/django-oscar>`_. This repository is home to all front-end and back-end code used to manage edX's product catalog and handle orders for those products, and houses extensions of the Oscar core which are specific to edX's needs. Many of the models in this project override abstract models present in Oscar.

Getting Started
---------------

Most commands necessary to run and develop the ecommerce service can be found in the included Makefile.

To install requirements necessary for local development, run::

    $ make requirements

``requirements/production.txt`` will install the packages needed to run the ecommerce service in a production setting.

To apply migrations, run::
    
    $ make migrations

Setup countries (for addresses) using the following command::

    $ python manage.py oscar_populate_countries

To stand up the development server, run::

    $ make serve

By default, the Django Debug Toolbar is disabled. To enable it, set the ENABLE_DJANGO_TOOLBAR environment variable.

Testing
-------

To run the unit test suite followed by quality checks, run::

    $ make validate

Acceptance Testing
~~~~~~~~~~~~~~~~~~

Before you beginning to run the acceptance tests, it is important to
make sure that **both** the LMS and eCommerce repos have switched to the
master branch and are completely up-to-date:

::

    $ git checkout master
    $ git pull

Testing Authentication and Enrollment
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To begin, boot up the `LMS VirtualBox
Server <https://github.com/edx/configuration/wiki/edX-Developer-Stack#installing-the-edx-developer-stack>`__
alongside the `eCommerce
Server <https://github.com/edx/ecommerce#getting-started>`__. Once in
the SSH session with the LMS machine, run the following two commands:

::

    $ sudo su edxapp
    $ sudo vi ../lms.env.json

Vi is used as the text editor in this example, but any text editor will
suffice. Once the JSON file is open, navigate to the 'OAuth' section and
append the following information:

::

    ENABLE_OAUTH2_PROVIDER: true,
    OAUTH_ENFORCE_SECURE: false,
    OAUTH_ENFORCE_CLIENT_SECURE: false,
    OAUTH_OIDC_ISSUER: "http://127.0.0.1:8000/oauth2"

If any of the above keys currently exist in the file, simply change
their value. Restart the LMS server session to enforce these changes.
Once the session has restarted, a Django superuser account must be
created. This can be done by navigating to ``http://127.0.0.1:8000`` and
signing up for a new edX account. Once this is completed, follow
`these <https://gist.github.com/antoviaque/8423488>`__ instructions to
grant the new account superuser privileges.

Once superuser status is in place, navigate to
``http://127.0.0.1:8000/admin`` and log in with the new credentials.
From here, add a new client with the following properties:

::

    User: {ID of superuser}
    Url:  http://localhost:8002/
    Redirect url: http://localhost:8002/complete/edx-oidc/
    Client type: Confidential

Click *Save*. Next, add this client as a trusted client by clicking on
the *Add* button next to "Trusted Clients". Lastly, add an access token
for the new client bt clicking the *Add* button next to "Access Tokens".
Set "Client" to the client just created, and make sure that the
expiration date is sometime into the future. Once this step is
completed, close out of the admin panel.

Now, we must ensure that the eCommerce configuration files reflects
these changes. In the eCommerce code repository, open the configuration
file ``/acceptance_tests/config.py``. Ensure that ``ACCESS_TOKEN`` and
``ECOMMERCE_API_SIGNING_KEY`` are both set to the access token we
generated earlier.

After these settings are confirmed, open
``/ecommerce/settings/local.py``. Ensure that
``SOCIAL_AUTH_EDX_OIDC_KEY`` is set to the client ID of the superuser
client and that ``SOCIAL_AUTH_EDX_OIDC_SECRET`` is set to the
superuser's client secret (both of these values can be found in the LMS
admin panel under "Clients"). ``JWT_AUTH['JWT_SECRET_KEY']`` should be
set to the same access token used for ``ACCESS_TOKEN`` and
``ECOMMERCE_API_SIGNING_KEY`` in ``config.py``. Restart the eCommerce
server for the changes to take effect.

Now, in order to test user authentication, navigate to the root
directory of the eCommerce repo and run\*:

::

    APP_SERVER_URL="http://localhost:8002" LMS_URL="http://127.0.0.1:8000" LMS_USERNAME="<LMS-SU-USERNAME>" LMS_EMAIL="<LMS-SU-EMAIL>" LMS_PASSWORD="<LMS-SU-PASSWORD>" ACCESS_TOKEN="<ACCESS-TOKEN>" HTTPS_RECEIPT_PAGE="False" ENABLE_LMS_AUTO_AUTH=True nosetests acceptance_tests/test_auth.py

Likewise, to test course enrollment, run the following\*:

::

    APP_SERVER_URL="http://localhost:8002" LMS_URL="http://127.0.0.1:8000" LMS_USERNAME="<LMS-SU-USERNAME>" LMS_EMAIL="<LMS-SU-EMAIL>" LMS_PASSWORD="<LMS-SU-PASSWORD>" ACCESS_TOKEN="<ACCESS-TOKEN>" HTTPS_RECEIPT_PAGE="False" ENABLE_LMS_AUTO_AUTH=True nosetests acceptance_tests/test_login_enrollment.py

Testing Cybersource and PayPal Payments
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*Please note that in order to complete this section, all steps described
in Section 1 must be completed first.*

To test Cybersource and PayPal payments, developer accounts on both
sites are required. Once the accounts are established, place the account
information (such as account ID and secret) in
``PAYMENT_PROCESSOR_CONFIG`` at the bottom of ``local.py``. Restart the
eCommerce server for changes to take effect.

Next, launch the edX Studio server (CMS). This can be done by following
`these <https://github.com/edx/configuration/wiki/edX-Developer-Stack#studio-workflow>`__
steps. Once started, open edX Studio by navigating to
``http://127.0.0.1:8001``. Add a new course with an arbitrary name,
organization, number, and run. However, make sure that all of these
fields are memorable, as they'll be needed later. If desired, the course
materials can be imported from any course currently on `the live
site <http://studio.edx.org>`__. Once the course is added, navigate back
to the homepage and click on the new course. In the address bar, the URL
will end in something similar to "edX/{Number}/{Run}". This is the
course key/ID.

Next, open the Oscar dashboard at ``http://localhost:8002`` and log in
with superuser credentials. Once the dashboard is open, select
"Products" under the "Catalouge" tab. Add a new product of type "Seat"
and fill it out with the new course information. Under the "Categories"
tab, set the category to type "Seat". Under the "Attributes" tab, set
the course key to the course key of the new course. Set the
certification type to type "verified".

Under the "Variants" tab, click "Add Variant". Under "Product Details",
give the variant the name "Honor" with an arbitrary UPC. Under
"Attributes", set the certificate type to "honor" and the course key to
the same course key from earlier. Under "Stock and Pricing", set the
partner to "edX" and set the "Price (excl tax)" to zero (0). Make sure
to set the SKU to something you can remember. We recommend using a SKU
like "honor" or "honorVariant". Once you are finished, click "Save and
add another variant".

For the second variant, set the name to "Verified" and a UPC different
than the UPC of the previous variant. Set the certificate type to
"verified" and set the course key to the same course key as the previous
variant. Under "Stock and Pricing", keep the same settings as the
previous variant, but change the "Price (excl tax)" to a number other
than zero. We would recommend a number somewhere between 15 and 20. Also
change the SKU to something specific to the verified variant, such as
"verified" or "verifiedVariant". When finished, click "Save".

Lastly, navigate back to the LMS admin panel
(http://127.0.0.1:8000/admin). Select "Course Modes" and click "Add
course mode". From here, add two course modes that refect the settings
specified in the two variants that were just created. Ensure that the
currencies match as well (in the LMS admin panel, the currency must be
lowercase).

Now, in order to test payment, navigate to the root directory of the
eCommerce repo and run\*:

::

    APP_SERVER_URL="http://localhost:8002" LMS_URL="http://127.0.0.1:8000" LMS_USERNAME="<LMS-SU-USERNAME>" LMS_EMAIL="<LMS-SU-EMAIL>" LMS_PASSWORD="<LMS-SU-PASSWORD>" ACCESS_TOKEN="<ACCESS-TOKEN>" HTTPS_RECEIPT_PAGE="False" ENABLE_LMS_AUTO_AUTH=True PAYPAL_EMAIL="<PAYPAL-DEVELOPER-EMAIL>" PAYPAL_PASSWORD="<PAYPAL-DEVELOPER-PASSWORD>" VERIFIED_COURSE_ID="<VERIFIED-COURSE-KEY>" nosetests acceptance_tests/test_payment.py

Running All Tests
^^^^^^^^^^^^^^^^^

In order to run all tests, complete all of the steps above, then run the
following command\*:

::

    APP_SERVER_URL="http://localhost:8002" LMS_URL="http://127.0.0.1:8000" LMS_USERNAME="<LMS-SU-USERNAME>" LMS_EMAIL="<LMS-SU-EMAIL>" LMS_PASSWORD="<LMS-SU-PASSWORD>" ACCESS_TOKEN="<ACCESS-TOKEN>" HTTPS_RECEIPT_PAGE="False" ENABLE_LMS_AUTO_AUTH=True PAYPAL_EMAIL="<PAYPAL-DEVELOPER-EMAIL>" PAYPAL_PASSWORD="<PAYPAL-DEVELOPER-PASSWORD>" VERIFIED_COURSE_ID="<VERIFIED-COURSE-KEY>" make accept

\*All strings in curly brackets must be replaced before running


Documentation |ReadtheDocs|_ 
----------------------------
.. |ReadtheDocs| image:: https://readthedocs.org/projects/edx-ecommerce/badge/?version=latest
.. _ReadtheDocs: http://edx-ecommerce.readthedocs.org/en/latest/

License
-------

The code in this repository is licensed under the AGPL unless otherwise noted. Please see ``LICENSE.txt`` for details.

How To Contribute
-----------------

Contributions are welcome. Please read `How To Contribute <https://github.com/edx/edx-platform/blob/master/CONTRIBUTING.rst>`_ for details. Even though it was written with ``edx-platform`` in mind, these guidelines should be followed for Open edX code in general.

Reporting Security Issues
-------------------------

Please do not report security issues in public. Please email security@edx.org.

Mailing List and IRC Channel
----------------------------

You can discuss this code on the `edx-code Google Group <https://groups.google.com/forum/#!forum/edx-code>`_ or in the ``#edx-code`` IRC channel on Freenode.
