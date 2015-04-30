import json
import logging
import os

from django.core.management import BaseCommand
import requests


API_TOKEN = 'ade25de268b47d3b5285d3e4fb90fdd20f544d85'
LMS_HOST = 'https://courses.stage.edx.org'

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Retrieve courses from LMS'

    def handle(self, *args, **options):
        # Get list of courses from LMS
        course_ids = []
        page = False #1
        num_pages = '(unknown)'
        headers = {'Authorization': 'Bearer {0}'.format(API_TOKEN)}


        filepath = os.path.abspath(os.path.join(os.path.dirname(__file__), 'courses.json'))
        with open(filepath) as data_file:
            course_ids = json.load(data_file)

        while page:
            try:
                logger.debug('Retrieving course info page %d of %s...', page, num_pages)
                url = '{host}/api/course_structure/v0/courses/?page={page}&page_size=100'.format(host=LMS_HOST,
                                                                                                 page=page)
                response = requests.get(url, headers=headers)
                response = response.json()
                num_pages = response['num_pages']
                course_details = response['results']
                course_ids += [course['id'] for course in course_details]

                if response['next']:
                    page += 1
                else:
                    page = None
                    logger.debug('Retrieved %d courses.', len(course_ids))
            except Exception as e:
                logger.exception("Unable to retrieve course data.")
                page = None
                return

        # Iterate over courses and retrieve modes
        course_modes = {}
        known_modes = set()

        # TODO Handle throttling
        for course_id in course_ids:
            url = '{host}/api/enrollment/v1/course/{course_id}'.format(host=LMS_HOST, course_id=course_id)
            response = requests.get(url).json()
            modes = [mode['slug'] for mode in response['course_modes']]
            known_modes.union(modes)
            course_modes[course_id] = modes

        # TODO Write data to file
        for course_id, modes in course_modes.iteritems():
            print '{}\t{}'.format(course_id, ','.join(modes))
