import abc
import urllib

from bok_choy.page_object import PageObject
from bok_choy.promise import EmptyPromise

from acceptance_tests.config import BASIC_AUTH_USERNAME, BASIC_AUTH_PASSWORD, APP_SERVER_URL, LMS_URL


# App page for ecommerce
class EcommerceAppPage(PageObject):  # pylint: disable=abstract-method
    path = None

    # Returns the URL of the page
    @property
    def url(self):
        return self.page_url

    # Instantiates the page
    def __init__(self, browser, path=None):
        super(EcommerceAppPage, self).__init__(browser)
        path = path or self.path
        self.server_url = APP_SERVER_URL
        self.page_url = '{0}/{1}'.format(self.server_url, path)


# The dashboard page
class DashboardHomePage(EcommerceAppPage):
    path = ''

    # Returns a boolean denoting whether the browser is currently viewing the dashboard
    def is_browser_on_page(self):
        return self.browser.title.startswith('Dashboard | Oscar')


# Page for LMS
class LMSPage(PageObject):  # pylint: disable=abstract-method
    __metaclass__ = abc.ABCMeta

    # Generates the authentication URL
    def _build_url(self, path):
        url = '{0}/{1}'.format(LMS_URL, path)

        if BASIC_AUTH_USERNAME and BASIC_AUTH_PASSWORD:
            url = url.replace('://', '://{0}:{1}@'.format(BASIC_AUTH_USERNAME, BASIC_AUTH_PASSWORD))

        return url


# LMS login page
class LMSLoginPage(LMSPage):

    # Generates the proper URL
    def url(self, course_id=None):  # pylint: disable=arguments-differ
        url = self._build_url('login')

        if course_id:
            params = {'enrollment_action': 'enroll', 'course_id': course_id}
            url = '{0}?{1}'.format(url, urllib.urlencode(params))

        return url

    # Is the browser currently viewing the page?
    def is_browser_on_page(self):
        return self.browser.title.startswith('Sign in')

    # Is the browser currently viewing the dashboard?
    def _is_browser_on_lms_dashboard(self):
        return lambda: self.browser.title.startswith('Dashboard')

    # Logs the user in
    def login(self, username, password):
        self.q(css='input#login-email').fill(username)
        self.q(css='input#login-password').fill(password)
        self.q(css='button.login-button').click()

        # Wait for LMS to redirect to the dashboard
        EmptyPromise(self._is_browser_on_lms_dashboard(), "LMS login redirected to dashboard").fulfill()


# Course mode page for LMS
class LMSCourseModePage(LMSPage):

    # Is the browser currently viewing the page?
    def is_browser_on_page(self):
        return self.browser.title.lower().startswith('enroll in')

    # Builds the correct URL for course modes
    @property
    def url(self):
        path = 'course_modes/choose/{}/'.format(urllib.quote_plus(self.course_id))
        return self._build_url(path)

    # Instantiates the page
    def __init__(self, browser, course_id):
        super(LMSCourseModePage, self).__init__(browser)
        self.course_id = course_id
