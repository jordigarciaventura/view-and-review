
Feature: Make a review of a Movie
    In order to be able to make reviews
    I want to be able to view a movie and make a review

Background: There is a registered user and a movie
    Given Exists a user "admin" with password "admin"
    Given A movie "156231" exists

Scenario: I can make a review of a movie
    Given I login as user "admin" with password "admin"
    Given Exists a rating for movie "156231" from user "admin" with score "2"
    When I view a movie "156231"
    Then I can make a review
        | id_title  | id_content |
        | title     | content    |
        
Scenario: I can edit my review of a movie
    Given Exists a rating for movie "156231" from user "admin" with score "2"
    Given A review of movie "156231" from user "admin" exists
        | title | content |
        | title | content |
    When I view a movie "156231"
    Then I can edit my review