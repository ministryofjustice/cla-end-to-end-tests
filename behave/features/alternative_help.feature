Feature: Assign alternative help to out of scope case.

Background: Login
    Given that I am logged in

@althelp
Scenario: Assign alternative help for out of scope user with necessary details
    GIVEN I am on the 'call centre dashboard' page
    WHEN I select to 'Create a case'
    AND I complete the users details with 'Test Dummy User' details
    AND I navigate back to the call centre dashboard
    AND I go back to the previous case
    AND I see the users previously entered details
    AND I select ‘Create Scope Diagnosis'
    AND I select the diagnosis <category> and click next <number> times
    | category                                                | number |
    | Crime                                                   | 2      |
    AND I get an "OUTOFSCOPE" decision
    #This is the icon in the top RH corner
    AND I click on the Assign Alternative Help icon
    AND I am taken to the "Alternative help" page for the case located at "/alternative_help/"
    THEN I select "Face to Face" and I am taken to a new tab displaying FALA


