from datetime import datetime, timedelta

from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User

from models import *

class TestEvents(TestCase):
    def setUp(self):
        testcase_username = 'testcase'
        self.testcase_password = testcase_password = User.objects.make_random_password()
        testcase_email = 'trmonks@gmail.com'

        self.user = User.objects.create_user(
            username=testcase_username,
            password=testcase_password,
            email=testcase_email,
        )

        self.client = Client()

        lan = EventType.objects.create(
            name="LAN Party",
            info="Smelly and fun.",
            target="GAM",
        )

        lib2 = Location.objects.create(
            name="Lib 2",
            description="Next to the side entrance to cafe library",
            image_url="",
            map_loc="",
        )

        self.event = Event.objects.create(
            type=lan,
            location=lib2,
            shortDescription="first LAN evuh",
            longDescription="blah blah blah",

            start=datetime.now() + timedelta(weeks=1),
            finish=datetime.now() + timedelta(weeks=2),
            displayFrom=datetime.now(),

            cancelled=False
        )

        self.hidden_event = Event.objects.create(
            type=lan,
            location=lib2,
            shortDescription="secret LAN",
            longDescription="this LAN is secret for now",

            start=datetime.now() + timedelta(weeks=2),
            finish=datetime.now() + timedelta(weeks=3),
            displayFrom=datetime.now() + timedelta(weeks=1),

            cancelled=False
        )

        layout = SeatingRoom.objects.create(
            room=lib2,
            name="default lib2",
            max_cols=10,
            max_rows=10,
        )

        SeatingRevision.objects.create(
            event=self.event,
            creator=self.user,
            number=1,
            comment="nobody",
        )

        EventSignup.objects.create(
            event=self.event,
            signupsLimit=60,

            open=datetime.now(),
            fresher_open=datetime.now(),
            guest_open=datetime.now(),

            close=datetime.now() + timedelta(weeks=1),
            seating=layout,
        )

    def login(self):
        successful = self.client.login(
            username=self.user.username,
            password=self.testcase_password,
        )

        if not successful:
            raise Exception("Couldn't login with test client")

    def logged_in(test):
        def wrapped(self, *args, **kwargs):
            self.login()
            return test(self, *args, **kwargs)

    def test_get_index_gives_code_200(self):
        response = self.client.get('/events/')
        self.assertEqual(response.status_code, 200)

    def test_index_contains_events_currently_displaying(self):
        response = self.client.get('/events/')
        self.assertContains(response, '<a href="/events/details/1/">', count=1, status_code=200)

    def test_index_doesnt_contain_events_not_displaying(self):
        response = self.client.get('/events/')
        self.assertContains(response, '<a href="/events/details/2/">', count=0, status_code=200)

    def test_get_calendar_gives_code_200(self):
        response = self.client.get('/events/calendar/')
        self.assertEqual(response.status_code, 200)

    def test_get_stats_without_login_redirects_to_login(self):
        response = self.client.get('/events/activity/')
        self.assertRedirects(response, '/login/?next=/events/activity/')

    @logged_in
    def test_get_stats_with_in_login_redirects_to_login(self):
        response = self.client.get('/events/activity/')
        self.assertEquals(response.status_code, 200)

    def test_get_event_that_exists_returns_200(self):
        response = self.client.get('/events/details/1/')
        self.assertEqual(response.status_code, 200)

    def test_get_event_that_exists_has_right_description(self):
        response = self.client.get('/events/details/1/')
        self.assertContains(response, "blah blah blah", count=1, status_code=200)

    def test_get_event_that_doesnt_exist_returns_404(self):
        response = self.client.get('/events/details/9001/')
        self.assertEqual(response.status_code, 404)

    @logged_in
    def test_signup_to_event_adds_row(self):
        response = self.client.post('/events/signup/1/')
        self.assertEqual(self.event.signup_set.count(), 1)
        self.assertEqual(self.event.signup_set.all()[0], self.user)

    def test_get_location_that_exists_returns_200(self):
        response = self.client.get('/events/location/1/')
        self.assertEqual(response.status_code, 200)

    def test_get_location_that_doesnt_exist_returns_404(self):
        response = self.client.get('/events/location/9001/')
        self.assertEqual(response.status_code, 404)

    def test_get_seating_plan_revision_that_exists_returns_200(self):
        response = self.client.get('/events/seating/1/1/')
        self.assertEqual(response.status_code, 200)

    def test_get_seating_plan_revision_that_doesnt_exist_returns_404(self):
        response = self.client.get('/events/seating/1/300/')
        self.assertEqual(response.status_code, 404)
