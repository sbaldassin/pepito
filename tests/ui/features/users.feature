Feature: Users registration and login

    Scenario: Users should be able to login
        Given I navigate to the home page
        When I complete the sign in form
        Then I am able to login
