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

    Create new case for existing user

    Search for existing user with a case and create new case
    As a CHS operator, I need the ability to search for an existing case and look at the search result,
    so I can select the relevant client case and proceed to create a new case for the client.
    Search is by client name

Background: Login
    Given I am logged in as "CHS_GENERAL_USER"

@createuser
Scenario: Create a Case and new User.
    Given I am on the 'call centre dashboard' page
    When I select to 'Create a case'
    Then I am taken to the 'case details' page
    And I select 'Create new user'
    And enter the client's personal details
    And I click the save button on the screen
    Then I will see the users details


@create_case_existing_user
Scenario: Create new case for existing user
  Given I am on the 'call centre dashboard' page
  When I search for a client name with an existing case
  Then I am taken to search results that shows cases belonging to that client
  And I select the name hyperlink for an existing case
  And I select the button to create a case for the client originally searched for
