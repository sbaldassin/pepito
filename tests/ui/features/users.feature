Feature: Users registration and login

    Scenario: User should be able to login
        Given I navigate to the home page
        When I complete the sign in form
        Then I am able to login


    Scenario: User should be able to reset their password
        Given I navigate to reset password page
        And I reset the password
        Then I get an reset password email

