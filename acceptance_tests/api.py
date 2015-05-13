import requests
from requests.auth import AuthBase

from acceptance_tests.config import ENROLLMENT_API_URL, ENROLLMENT_API_TOKEN


# Attaches Bearer Authentication to the given Request object.
class BearerAuth(AuthBase):

    # Instantiates the auth class
    def __init__(self, token):
        self.token = token

    # Update the request headers.
    def __call__(self, r):
        r.headers['Authorization'] = 'Bearer {}'.format(self.token)
        return r


# The enrollment API client
class EnrollmentApiClient(object):

    # Instantiates the enrollment class
    def __init__(self, host=None, key=None):
        self.host = host or ENROLLMENT_API_URL
        self.key = key or ENROLLMENT_API_TOKEN

    # Retrieves the enrollment status for given user in a given course
    def get_enrollment_status(self, username, course_id):
        url = '{host}/enrollment/{username},{course_id}'.format(host=self.host, username=username, course_id=course_id)
        return requests.get(url, auth=BearerAuth(self.key)).json()
