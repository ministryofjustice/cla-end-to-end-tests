Feature: Assign alternative help to out of scope case.

Background: Login
    Given that I am logged in

@althelp
Scenario: Create user and out of scope case
    GIVEN that I am on the 'call centre dashboard' page
    WHEN I select to 'Create a case'
    THEN I complete the users details with 'Test Dummy User' details
    THEN I navigate the call centre dashboard
    THEN I go back to the previous case
    THEN I should see the users previously entered details
    WHEN I select ‘Create Scope Diagnosis'
    AND I select the diagnosis <category> and click next <number> times
    | category                                                | number |
    | Crime                                                   | 2      |
    THEN I get an OUTOFSCOPE decision