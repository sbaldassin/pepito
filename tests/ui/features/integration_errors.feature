Feature: Integration errors page interactions

    Scenario: User should be able to see the integration errors
        Given I navigate to the home page
        When I complete the sign in form
        Then I am able to login
        Then I verify the total integration errors
        When I click in integration errors button
        Then I verify the page title

    Scenario: User should be able to delete all the integration errors
        Given I navigate to the home page
        When I complete the sign in form
        Then I am able to login
        When I click in integration errors button
        Then I verify the page title
        Then I click on delete all button
        When I click on confirm button
        Then I verify that there are no messages left

