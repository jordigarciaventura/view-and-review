Feature: View a movie
    In order to check the details of a movoie
    I want to be able to check a movie
        
Background: There is a registered user
    Given Exists a user "admin" with password "admin"

Scenario: View a movie
    When I view a movie "156231"
    Then I'm viewing the movie page for movie "156231"
    
Scenario: I can make a review of movie
    Given I login as user "admin" with password "admin"
    Given Exists a rating for movie "156231" from user "admin"
    Then User "admin" can make a review for movie "156231"
