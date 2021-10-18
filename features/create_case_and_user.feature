Feature: Case and user creation.
    Confirming that a case can be created and then a new User 
    linked with the case.

    Minimal data for creating the user is: 
     - minimum name
     - address
     - date of birth
     - phone number
     - national insurance number
     - adaptations
     - media code
     - source

Scenario: Create a Case and new User.
    Given that I am on the call centre dashboard page.
    When I select to 'Create a case'.
    Then I am taken to the 'case details' page.
    And I select 'Create new user'.
    And enter the client's personal details.
    And I click the save button on the screen. 
    Then I will see the users details.