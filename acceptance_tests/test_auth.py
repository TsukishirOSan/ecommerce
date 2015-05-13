from unittest import skipUnless

from bok_choy.web_app_test import WebAppTest

from acceptance_tests.config import ENABLE_OAUTH_TESTS
from acceptance_tests.mixins import LoginMixin
from acceptance_tests.pages import DashboardHomePage

# Tests OAuth2 logins
@skipUnless(ENABLE_OAUTH_TESTS, 'OAuth tests are not enabled.')
class OAuth2FlowTests(LoginMixin, WebAppTest):
    
    # Set up the test
    def setUp(self):
        """
        Instantiate the page objects.
        """
        super(OAuth2FlowTests, self).setUp()

        self.app_login_page = DashboardHomePage(self.browser)

    # Tests the log in
    def test_login(self):
        """
        Note: If you are testing locally with a VM and seeing signature expiration errors, ensure the clocks of the VM
        and host are synced within at least one minute (the default signature expiration time) of each other.
        """
        self.login_with_lms()

        # Visit login URL and get redirected
        self.app_login_page.visit()
