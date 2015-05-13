import logging
import uuid

import requests
from ecommerce_api_client.client import EcommerceApiClient

from acceptance_tests.api import EnrollmentApiClient
from acceptance_tests.config import (ENABLE_LMS_AUTO_AUTH, APP_SERVER_URL, LMS_PASSWORD, LMS_EMAIL, LMS_URL,
                                     BASIC_AUTH_USERNAME, BASIC_AUTH_PASSWORD, ECOMMERCE_API_SERVER_URL,
                                     LMS_USERNAME, ECOMMERCE_API_TOKEN)
from acceptance_tests.pages import LMSLoginPage

log = logging.getLogger(__name__)

# Used to login
class LoginMixin(object):
    
    # Instantiates the login
    def setUp(self):
        super(LoginMixin, self).setUp()
        self.lms_login_page = LMSLoginPage(self.browser)

    # Logs in with LMS
    def login(self):
        self.login_with_lms()

    # Helper function for login()
    def login_with_lms(self, email=None, password=None, course_id=None):
        """ Visit LMS and login. """
        email = email or LMS_EMAIL
        password = password or LMS_PASSWORD

        # Note: We use Selenium directly here (as opposed to bok-choy) to avoid issues with promises being broken.
        self.lms_login_page.browser.get(self.lms_login_page.url(course_id))  # pylint: disable=not-callable
        self.lms_login_page.login(email, password)


# Used to logout
class LogoutMixin(object):
    
    # Logs out
    def logout(self):
        url = '{}/accounts/logout/'.format(APP_SERVER_URL)
        self.browser.get(url)

# Retrieves info about the user
class LmsUserMixin(object):
    password = 'edx'

    # Gets the user credentials
    def get_lms_user(self):
        
        # If using auto_auth, we create a new user
        if ENABLE_LMS_AUTO_AUTH:
            return self.create_lms_user()

        # If not, return the user's current info
        return LMS_USERNAME, LMS_PASSWORD, LMS_EMAIL

    # Creates new auto auth user
    def create_lms_user(self, username=None, password=None, email=None):
        username = username or ('auto_auth_' + uuid.uuid4().hex[0:20])
        password = password or 'edx'
        email = email or '{}@example.com'.format(username)

        url = '{host}/auto_auth?no_login=true&username={username}&password={password}&email={email}'.format(
            host=LMS_URL, username=username, password=password, email=email)
        auth = None

        if BASIC_AUTH_USERNAME and BASIC_AUTH_PASSWORD:
            auth = (BASIC_AUTH_USERNAME, BASIC_AUTH_PASSWORD)

        requests.get(url, auth=auth)

        return username, password, email

# Assertments for the enrollment API
class EnrollmentApiMixin(object):
    def setUp(self):
        super(EnrollmentApiMixin, self).setUp()
        self.enrollment_api_client = EnrollmentApiClient()

    def assert_user_enrolled(self, username, course_id, mode='honor'):
        status = self.enrollment_api_client.get_enrollment_status(username, course_id)
        self.assertDictContainsSubset({'is_active': True, 'mode': mode}, status)

# Assertments for the ecommerce api
class EcommerceApiMixin(object):
    @property
    def ecommerce_api_client(self):
        return EcommerceApiClient(ECOMMERCE_API_SERVER_URL, oauth_access_token=ECOMMERCE_API_TOKEN)

    def assert_order_created_and_completed(self):
        orders = self.ecommerce_api_client.orders.get()['results']
        self.assertGreater(len(orders), 0, 'No orders found for the user!')

        # TODO Validate this is the correct order.
        order = orders[0]

        self.assertEqual(order['status'], 'Complete')
