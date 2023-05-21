Feature: Make a rating of a film
    In order to make a rating of a film
    I should be able to make a rating
    
Background: There is a registered user and movie
    Given Exists a user "admin" with password "admin"
    Given I login as user "admin" with password "admin"
    Given A movie "1283" exists
    
Scenario: I can make a rating of a movie
    When I make a rating of score "3" of the movie "1283"
    Then There is "1" ratings

Scenario: I can delete my rating of a movie
    Given Exists a rating for movie "1283" from user "admin" with score "3"
    When I can delete a rating of the movie "1283"
    Then There is "0" ratings
    
Scenario: I can edit my rating of a movie
    Given Exists a rating for movie "1283" from user "admin" with score "3"
    When I can edit a rating with new score "5" of the movie "1283"