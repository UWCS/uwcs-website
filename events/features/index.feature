Feature: Event index

    Scenario: No events
        Given I access the url "/events/"
        Then I see the title "Events List - University of Warwick Computing Society"
        And I see a notification that "There are no upcoming events scheduled"

    Scenario: Upcoming event
        Given there is a "LAN Party" running 1 weeks from now for 2 hours in "Lib2"
        When I access the url "/events/"
        Then I see 1 event
        And I see a "LAN Party" scheduled

    Scenario: Multiple upcoming events
        Given there is a "LAN Party" running 1 weeks from now for 2 hours in "Lib2"
        And there is a "LAN Party" running 2 weeks from now for 2 hours in "Lib2"
        When I access the url "/events/"
        Then I see 2 events

    Scenario: Upcoming hidden event
        Given there is a "LAN Party" running 1 weeks from now for 2 hours in "Lib2"
        And the event is set to display from 1 weeks from now
        When I access the url "/events/"
        Then I see a notification that "There are no upcoming events scheduled"

    Scenario: Upcoming cancelled event
        Given there is a "LAN Party" running 1 weeks from now for 2 hours in "Lib2"
        And the event is cancelled
        When I access the url "/events/"
        Then I see a notification that "There are no upcoming events scheduled"

    Scenario: Event in the past
        Given there is a "LAN Party" running 1 weeks ago for 2 hours in "Lib2"
        When I access the url "/events/"
        Then I see a notification that "There are no upcoming events scheduled"
