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


    Scenario: Users should be able to upload freespin data
        Given I have a csv with freespin data
        When I navigate to the home page
        And I complete the sign in form
        And I am able to login
        And I navigate to the dimensions data page
        And I click on freespin tab
        Then I am able to upload freespin data
        And the freespins are saved in the db


    Scenario: Users should be able to upload bonus dimensions data
        Given I have a csv with bonus data
        When I navigate to the home page
        And I complete the sign in form
        And I am able to login
        And I navigate to the dimensions data page
        And I click on bonuses tab
        Then I am able to upload bonus data
        And the bonuses are saved in the db


    Scenario: Users should be able to upload bonus facts data
        Given I have a csv with bonus facts data
        When I navigate to the home page
        And I complete the sign in form
        And I am able to login
        And I navigate to the facts data page
        And I select the Bonuses tab
        Then I am able to upload bonus fact data
        And The bonuses are saved in the db


    Scenario: Users should be able to upload Free spins facts data
        Given I have a csv with free spins facts data
        When I navigate to the home page
        And I complete the sign in form
        And I am able to login
        And I navigate to the facts data page
        And I select the Free spins tab
        Then I am able to upload free spins fact data
        And The free spins are saved in the db


    Scenario: Users should be able to upload casino games facts data
        Given I have a csv with casino games facts data
        When I navigate to the home page
        And I complete the sign in form
        And I am able to login
        And I navigate to the facts data page
        And I select the Game sessions (casino) tab
        Then I am able to upload game sessions fact data
        And The game session facts are saved in the db


    Scenario: Users should be able to upload casino wagers facts data
        Given I have a csv with casino wagers facts data
        When I navigate to the home page
        And I complete the sign in form
        And I am able to login
        And I navigate to the facts data page
        And I select the Casino wagers tab
        Then I am able to upload wagers casino fact data
        And The wagers are saved in the db


    Scenario: Users should be able to upload Sports wagers facts data
        Given I have a csv with sports wagers facts data
        When I navigate to the home page
        And I complete the sign in form
        And I am able to login
        And I navigate to the facts data page
        And I select the Sports wagers tab
        Then I am able to upload wagers sports fact data
        And The wagers are saved in the db


    Scenario: Users should be able to upload Lottery wagers facts data
        Given I have a csv with lottery wagers facts data
        When I navigate to the home page
        And I complete the sign in form
        And I am able to login
        And I navigate to the facts data page
        And I select the Lottery wagers tab
        Then I am able to upload wagers lottery fact data
        And The wagers are saved in the db


    Scenario: Users should be able to upload Parimutuel wagers facts data
        Given I have a csv with parimutuel wagers facts data
        When I navigate to the home page
        And I complete the sign in form
        And I am able to login
        And I navigate to the facts data page
        And I select the Parimutuel wagers tab
        Then I am able to upload wagers parimutuel fact data
        And The wagers are saved in the db


    Scenario: Users should be able to upload deposits facts data
        Given I have a csv with deposits facts data
        When I navigate to the home page
        And I complete the sign in form
        And I am able to login
        And I navigate to the facts data page
        And I select the Deposits tab
        Then I am able to upload deposits fact data
        And the deposits are saved in the db


    Scenario: Users should be able to upload withdrawals facts data
        Given I have a csv with withdrawals facts data
        When I navigate to the home page
        And I complete the sign in form
        And I am able to login
        And I navigate to the facts data page
        And I select the Withdrawals tab
        Then I am able to upload withdrawals fact data
        And the withdrawals are saved in the db


    Scenario: Users should be able to upload General Payouts facts data
        Given I have a csv with general payouts facts data
        When I navigate to the home page
        And I complete the sign in form
        And I am able to login
        And I navigate to the facts data page
        And I select the Payouts tab
        Then I am able to upload payouts fact data
        And The payouts are saved in the db


    Scenario: Users should be able to upload Casino Payouts facts data
        Given I have a csv with casino payouts facts data
        When I navigate to the home page
        And I complete the sign in form
        And I am able to login
        And I navigate to the facts data page
        And I select the Payouts tab
        Then I am able to upload payouts fact data
        And The payouts are saved in the db


    Scenario: Users should be able to upload Sports Payouts facts data
        Given I have a csv with sport payouts facts data
        When I navigate to the home page
        And I complete the sign in form
        And I am able to login
        And I navigate to the facts data page
        And I select the Payouts tab
        Then I am able to upload payouts fact data
        And The payouts are saved in the db


    Scenario: Users should be able to upload Bets Payouts facts data
        Given I have a csv with bet payouts facts data
        When I navigate to the home page
        And I complete the sign in form
        And I am able to login
        And I navigate to the facts data page
        And I select the Payouts tab
        Then I am able to upload payouts fact data
        And The payouts are saved in the db


    Scenario: Users should be able to upload Esport Payouts facts data
        Given I have a csv with esport payouts facts data
        When I navigate to the home page
        And I complete the sign in form
        And I am able to login
        And I navigate to the facts data page
        And I select the Payouts tab
        Then I am able to upload payouts fact data
        And The payouts are saved in the db


    Scenario: Users should be able to upload Lottery Payouts facts data
        Given I have a csv with lottery payouts facts data
        When I navigate to the home page
        And I complete the sign in form
        And I am able to login
        And I navigate to the facts data page
        And I select the Payouts tab
        Then I am able to upload payouts fact data
        And The payouts are saved in the db


    Scenario: Users should be able to upload Parimutuel Payouts facts data
        Given I have a csv with parimutuel payouts facts data
        When I navigate to the home page
        And I complete the sign in form
        And I am able to login
        And I navigate to the facts data page
        And I select the Payouts tab
        Then I am able to upload payouts fact data
        And The payouts are saved in the db