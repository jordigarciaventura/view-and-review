Feature: Make a rating of a film
    In order to make a rating of a film
    I should be able to make a rating
    
Background: There is a registered user and movie
    Given Exists a user "admin" with password "admin"
    Given A movie "156231" exists
    
Scenario: I can make a rating of a movie
    Given I login as user "admin" with password "admin"
    When I make a rating of score "3" of the movie "156231"
