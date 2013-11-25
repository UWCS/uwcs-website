from django.core.management import call_command
from django.test.client import Client
from django.test.testcases import disable_transaction_methods, restore_transaction_methods
from django.db import transaction

from lettuce import *
from lxml import html
from nose.tools import assert_equal
from hamcrest import *

from uwcs_website.events.models import *

@before.all
def setup_db():
    # TODO: should probably flush/syncdb here but SLOWWWWW
    pass

@before.all
def set_browser():
    world.browser = Client()

@before.each_scenario
def start_django_transaction(scenario):
    transaction.enter_transaction_management()
    transaction.managed(True)
    call_command('loaddata', 'events/fixtures/event-types.json', **{
        'verbosity': 0,
        'commit': False,
    })
    disable_transaction_methods()

@after.each_scenario
def rollback_django_transaction(scenario):
    restore_transaction_methods()
    transaction.rollback()
    transaction.leave_transaction_management()

@step(r'I access the url "(.*?)"')
def access_url(step, url):
    response = world.browser.get(url)
    world.dom = html.fromstring(response.content)

@step(r'I see the title "(.*?)"')
def see_title(step, text):
    title = world.dom.cssselect('title')[0]
    assert_equal(title.text, text)

def from_now(delta, delta_unit):
    return datetime.now() + timedelta(**{str(delta_unit): int(delta)})

def ago(delta, delta_unit):
    return datetime.now() - timedelta(**{str(delta_unit): int(delta)})

@step(r'there is a "(.*?)" running (\d+) (\w+) from now for (\d+) (\w+) in "(.*?)"')
def schedule_event(step, type, delta, delta_unit, duration, duration_unit, location):
    event_type = EventType.objects.get(name=type)
    location = Location.objects.get(name=location)

    start = from_now(delta, delta_unit)

    world.event = Event.objects.create(
        type=event_type,
        location=location,
        shortDescription="nothing to see here",
        longDescription="nothing to see here",
        start=start,
        finish=start + timedelta(**{str(duration_unit): int(duration)}),
    )

@step(r'there is a "(.*?)" running (\d+) (\w+) ago for (\d+) (\w+) in "(.*?)"')
def schedule_event(step, type, delta, delta_unit, duration, duration_unit, location):
    event_type = EventType.objects.get(name=type)
    location = Location.objects.get(name=location)

    start = ago(delta, delta_unit)

    world.event = Event.objects.create(
        type=event_type,
        location=location,
        shortDescription="nothing to see here",
        longDescription="nothing to see here",
        start=start,
        finish=start + timedelta(**{str(duration_unit): int(duration)}),
    )

@step(r'the event is set to display from (\d+) (\w+) from now')
def set_event_display_from(step, delta, delta_unit):
    display_from = from_now(delta, delta_unit)
    world.event.displayFrom = display_from
    world.event.save()

@step(r'the event has a seating plan')
def set_event_seating_plan(step):
    room = SeatingRoom.objects.create(
        room=world.event.location,
        name='seating plan',
        max_cols = 4,
        max_rows = 4
    )
    options = EventSignup.objects.create(
        event = world.event,
        signupsLimit = 0,
        open = datetime.now(),
        close = datetime.now() + timedelta(weeks=1),
        fresher_open = datetime.now(),
        guest_open = datetime.now(),
        seating = room,
    )

@step(r'the event is cancelled')
def set_event_cancelled(step):
    world.event.cancelled = True
    world.event.save()

@step(r'I see a notification that "(.*)"')
def see_notification(step, text):
    content = world.dom.cssselect('.notification')[0]
    assert_that(content.text, contains_string(text))

@step('I see (\d+) events?')
def see_events(step, n):
    world.listed_events = world.dom.cssselect('li.name')
    assert_that(world.listed_events, has_length(int(n)))

    if n == '1':
        world.subject = world.listed_events[0]

@step('the event description has a strike through it')
def strike_through(step):
    world.dom.cssselect('li.name > a')
    assert_that(world.subject.cssselect('del'), is_not(equal_to([])))

@step('I see a "(.*?)" scheduled')
def see_scheduled(step, event_type):
    event_names = world.dom.cssselect('li.name > a')
    event_names = map(lambda e: e.text, event_names)
    assert_that(event_names, has_item(event_type))
