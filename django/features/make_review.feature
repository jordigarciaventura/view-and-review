Feature: Make a review of a Movie
    In order to be able to make reviews
    I want to be able to view a movie and make a review

Background: There is a registered user and a movie
    Given Exists a user "admin" with password "admin"
    Given I login as user "admin" with password "admin"
    Given A movie "1283" exists

Scenario: I can make a review of a movie
    Given Exists a rating for movie "1283" from user "admin" with score "2"
    When I view a movie "1283"
    Then I can make a review
        | id_title  | id_content |
        | title     | content    |
        
Scenario: I can edit my review of a movie
    Given Exists a rating for movie "1283" from user "admin" with score "2"
    Given A review of movie "1283" from user "admin" exists
        | title | content |
        | title | content |
    When I view a movie "1283"
    Then I can edit my review
        | edit_id_title     | edit_id_content     |
        | new_title         | new_content         |
        
Scenario: I can delete my review of a movie
    Given Exists a rating for movie "1283" from user "admin" with score "2"
    Given A review of movie "1283" from user "admin" exists
        | title | content |
        | title | content |
    When I view a movie "1283"
    When I delete my review
    Then There are no reviews of movie "1283" by user "admin"