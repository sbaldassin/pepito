Feature: Campaign notifications interactions

    Scenario: User should be able to see the campaign notifications
        Given I navigate to the home page
        When I complete the sign in form
        Then I am able to login
        Then I verify the total campaign notifications
        When I click on campaign notifications button
        Then I verify the notification page title

    Scenario: User should cancel the delete all notifications action
        Given I navigate to the home page
        When I complete the sign in form
        Then I am able to login
        When I click on campaign notifications button
        Then I verify the notification page title
        Then I click on delete all notifications button
        When I click on cancel button

