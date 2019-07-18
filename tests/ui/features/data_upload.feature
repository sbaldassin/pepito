Feature: Data upload


    Scenario: Users should be able to upload users dimensions data
        Given I have a csv with 5 users
        When I navigate to the home page
        And I complete the sign in form
        And I am able to login
        And I navigate to the dimensions data page
        Then I am able to upload dimensions data
        And the users are saved in the db

    Scenario: Users should be able to upload games data
        Given I have a csv with 2 games
        When I navigate to the home page
        And I complete the sign in form
        And I am able to login
        And I navigate to the dimensions data page
        And I click on game tab
        Then I am able to upload games data
        And the games are saved in the db

