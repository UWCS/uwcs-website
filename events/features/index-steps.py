from django.core.management import call_command
from django.test.client import Client
from django.test.testcases import disable_transaction_methods, restore_transaction_methods
from django.db import transaction

from lettuce import *
from lxml import html
from nose.tools import eq_
from hamcrest import *

from events.models import *

@before.all
def setup_db():
    pass
    #call_command('syncdb', interactive=False)
    #call_command('flush', interactive=False)

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
    eq_(title.text, text)

@step(r'there is a "(.*?)" running (\d+) (\w+) from now for (\d+) (\w+) in "(.*?)"')
def schedule_event(step, type, delta, delta_unit, duration, duration_unit, location):
    event_type = EventType.objects.get(name=type)
    location = Location.objects.get(name=location)

    start = datetime.now() + timedelta(**{str(delta_unit): int(delta)})

    Event.objects.create(
        type=event_type,
        location=location,
        shortDescription="nothing to see here",
        longDescription="nothing to see here",
        start=start,
        finish=start + timedelta(**{str(duration_unit): int(duration)}),
    )

@step(r'I see a notification that "(.*)"')
def see_notification(step, text):
    content = world.dom.cssselect('.notification')[0]
    assert_that(content.text, contains_string(text))

@step('I see (\d+) events?')
def see_events(step, n):
    events = world.dom.cssselect('li.name')
    assert_that(events, has_length(int(n)))

@step('I see a "(.*?)" scheduled')
def see_scheduled(step, event_type):
    event_names = world.dom.cssselect('li.name > a')
    event_names = map(lambda e: e.text, event_names)
    assert_that(event_names, has_item(event_type))
