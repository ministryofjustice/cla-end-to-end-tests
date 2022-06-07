Feature: Search for existing user with a case and create new case
    As a CHS operator, I need the ability to search for an existing case and look at the search result,
    so I can select the relevant client case and proceed to create a new case for the client.
    Search is by client name

Background: Login
    Given that I am logged in

@create_case_existing_user
Scenario: Create new case for existing user
    Given that I am on the 'call centre dashboard' page
    When I search for a client name with an existing case
    Then I am taken to search results that shows cases belonging to that client
    And I select the name hyperlink for an existing case
    And I select the button to create a case for the client originally searched for


