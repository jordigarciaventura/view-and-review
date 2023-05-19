Feature: View a movie
    In order to check the details of a movie
    I want to be able to check a movie
        
Background: There is a registered user and a film
    Given Exists a user "admin" with password "admin"
    Given A movie "156231" exists
    

Scenario: View a movie
    When I view a movie "156231"
    Then I'm viewing the movie page for movie "156231"
    
