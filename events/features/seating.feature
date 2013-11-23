Feature: Event index

    Scenario: Visiting seating plan revision that doesn't exit
        Given there is a "LAN Party" running 1 weeks from now for 2 hours in "Lib2"
        And the event has a seating plan
        When I access the url "/events/seating/2/16/"
        Then I see a notification that "There is no such seating plan revision"
