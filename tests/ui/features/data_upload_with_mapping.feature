Feature: Data upload with mapping
    Scenario: Users should be able to upload customer data with mapping
        Given I have a csv with 2 rows with customer data with headers
        When I navigate to the home page
        And I complete the sign in form
        And I am able to login
        And I navigate to the dimensions data page
        And I click on data mapping section
        Then I am able to upload customer data with mapping
        Then I am able to map customer headers

    Scenario: Users should be able to upload freespin data with mapping
        Given I have a csv with 2 rows with freespin data with headers
        When I navigate to the home page
        And I complete the sign in form
        And I am able to login
        And I navigate to the dimensions data page
        And I click on freespin tab
        And I click on data mapping section
        Then I am able to upload freespin data with mapping
        Then I am able to map freespin headers

    Scenario: Users should be able to upload bonuses data with mapping
        Given I have a csv with 2 rows with bonuses data with headers
        When I navigate to the home page
        And I complete the sign in form
        And I am able to login
        And I navigate to the dimensions data page
        And I click on bonuses tab
        And I click on data mapping section
        Then I am able to upload bonuses data with mapping
        Then I am able to map bonuses headers


    Scenario: Users should be able to upload game data with mapping
        Given I have a csv with 2 rows with games data with headers
        When I navigate to the home page
        And I complete the sign in form
        And I am able to login
        And I navigate to the dimensions data page
        And I click on game tab
        And I click on data mapping section
        Then I am able to upload games data with mapping
        Then I am able to map games headers