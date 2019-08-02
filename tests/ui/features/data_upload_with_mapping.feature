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

    Scenario: Users should be able to upload bonus facts data with mapping
        Given I have a csv with bonus facts data and mappings
        When I navigate to the home page
        And I complete the sign in form
        And I am able to login
        And I navigate to the facts data page
        And I select the Bonuses tab
        And I select the data mapping section
        And I upload the bonus fact mappings
        And I complete the mappings for bonuses facts
        And I select the upload bonuses data section
        Then I am able to upload bonus fact data with mapping
        And The bonuses are saved in the db


    Scenario: Users should be able to upload free spins facts data with mapping
        Given I have a csv with free spins facts data and mappings
        When I navigate to the home page
        And I complete the sign in form
        And I am able to login
        And I navigate to the facts data page
        And I select the Free spins tab
        And I select the data mapping section
        And I upload the freespin fact mappings
        And I complete the mappings for free spins facts
        And I select the upload freespin data section
        Then I am able to upload free spins fact data with mappings
        And The free spins are saved in the db


    Scenario: Users should be able to upload casino wagers facts data with mapping
        Given I have a csv with casino wagers facts data and mappings
        When I navigate to the home page
        And I complete the sign in form
        And I am able to login
        And I navigate to the facts data page
        And I select the Casino wagers tab
        And I select the data mapping section
        And I upload the casino wager fact mappings
        And I complete the mappings for casino wagers facts
        And I select the upload wagers casino data section
        Then I am able to upload casino wagers fact data with mappings
        And The wagers are saved in the db

    @PEPE
    Scenario: Users should be able to upload sports wagers facts data with mapping
        Given I have a csv with sports wagers facts data and mappings
        When I navigate to the home page
        And I complete the sign in form
        And I am able to login
        And I navigate to the facts data page
        And I select the Sports wagers tab
        And I select the data mapping section
        And I upload the sports wager fact mappings
        And I complete the mappings for sport wagers facts
        And I select the upload wagers sports data section
        Then I am able to upload sport wagers fact data with mappings
        And The wagers are saved in the db