Feature: Vote a review of a Movie
    In order to be able to upvote or downvote
    I want to be able to view a review and make vote
    
Background: There is a registered User and Movie
    Given Exists a user "admin" with password "admin"
    Given I login as user "admin" with password "admin"
    Given A movie "1283" exists
    Given Exists a rating for movie "1283" from user "admin" with score "2"
    Given A review of movie "1283" from user "admin" exists
        | title | content |
        | title | content |
        
Scenario: I want to upvote a review of a Movie
    When I view a movie "1283"
    When I "upvote" the first review
    Then There are "1" review votes and their value is "True"
    
Scenario: I want to downvote a review of a Movie
    When I view a movie "1283"
    When I "downvote" the first review
    Then There are "1" review votes and their value is "False"
