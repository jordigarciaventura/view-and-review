Feature: Delete user
    In order to being able to delete your user
    I want to delete my user
    
Background: There is a registered user
    Given Exists a user "admin" with password "admin"
    
Scenario: Delete my user
    Given I login as user "admin" with password "admin"
    When I delete my user
    Then There are no users 
    And I'm viewing the main page