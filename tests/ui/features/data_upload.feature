Feature: Data upload


    @PEPE
    Scenario: Users should be able to upload dimensions data
        Given I navigate to the home page
        And I complete the sign in form
        And I am able to login
        When I navigate to the dimensions data page
        Then I am able to upload dimensions data

