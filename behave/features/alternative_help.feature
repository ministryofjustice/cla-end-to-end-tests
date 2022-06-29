Feature: Assign alternative help to out of scope case.

Background: Login
    Given that I am logged in as "CHS"

@alt_help_succeeds
Scenario: Assign alternative help for out of scope user with necessary details
    GIVEN I am on the 'call centre dashboard' page
    WHEN I select to 'Create a case'
    AND I complete the users details with FULL details
    AND I navigate back to the call centre dashboard
    AND I go back to the previous case
    AND I see the users previously entered FULL details
    AND I select ‘Create Scope Diagnosis'
    AND I select the diagnosis <category> and click next <number> times
    | category                                                | number |
    | Crime                                                   | 2      |
    AND I get an "OUTOFSCOPE" decision
    #This is the icon in the top RH corner
    AND I click on the Assign Alternative Help icon
    AND I am taken to the "Alternative help" page for the case located at "/alternative_help/"
    THEN I select "Face to Face" and I am taken to a new tab displaying FALA

@alt_help_fails_insufficient_user_details
Scenario: Assign alternative help for out of scope user without postcode or phone number
    GIVEN I am on the 'call centre dashboard' page
    WHEN I select to 'Create a case'
    AND I complete the users details with LIMITED details
    AND I navigate back to the call centre dashboard
    AND I go back to the previous case
    AND I select ‘Create Scope Diagnosis'
    AND I select the diagnosis <category> and click next <number> times
    | category                                                | number |
    | Crime                                                   | 2      |
    AND I get an "OUTOFSCOPE" decision
    #This is the icon in the top RH corner
    AND I click on the Assign Alternative Help icon
    THEN a Missing Information validation message is displayed to the user

