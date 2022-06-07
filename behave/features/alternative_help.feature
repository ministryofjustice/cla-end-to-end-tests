Feature: Assign alternative help to out of scope case.

Background: Login
    Given that I am logged in

@althelp
Scenario: Create user and out of scope case
    GIVEN  I am on the call centre dashboard
    WHEN I select to 'Create a case'
    THEN I complete the users details with 'Test Dummy User' details
    THEN I navigate the call centre dashboard
    THEN I go back to the previous case
    THEN I should see the users previously entered details