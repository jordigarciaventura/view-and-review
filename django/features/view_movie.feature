Feature: View a movie
    In order to check the details of a movoie
    I want to be able to check a movie
        
Scenario: View a movie
    When I view a movie "156231"
    Then I'm viewing the movie page for movie "156231"