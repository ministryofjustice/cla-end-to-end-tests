@cla_frontend
Feature: - Assign alternative help to out of scope case.
         - Assign a case to a specialist provider.
         - Assign face to face.
         - Diagnosis diagnosis journeys

Background: Login
    Given I am logged in as "CHS_GENERAL_USER"

# Assign alternative help to out of scope case.
@alt_help_succeeds
Scenario: Assign alternative help for out of scope user with necessary details
    Given I am on the 'call centre dashboard' page
    When I select to 'Create a case'
    And I complete the users details with FULL details
    And I navigate back to the call centre dashboard
    And I go back to the previous case
    And I see the users previously entered FULL details
    And I select ‘Create Scope Diagnosis'
    And I select the diagnosis <category> and click next <number> times
    | category                                                | number |
    | Crime                                                   | 2      |
    And I get an "OUTOFSCOPE" decision
    #This is the icon in the top RH corner
    And I click on the Assign Alternative Help icon
    And I am taken to the "Alternative help" page for the case located at "/alternative_help/"
    Then I select "Face to Face" and I am taken to a new tab displaying FALA

@alt_help_fails_insufficient_user_details
Scenario: Assign alternative help for out of scope user without postcode or phone number
    Given I am on the 'call centre dashboard' page
    When I select to 'Create a case'
    And I complete the users details with LIMITED details
    And I navigate back to the call centre dashboard
    And I go back to the previous case
    And I select ‘Create Scope Diagnosis'
    And I select the diagnosis <category> and click next <number> times
    | category                                                | number |
    | Crime                                                   | 2      |
    And I get an "OUTOFSCOPE" decision
    #This is the icon in the top RH corner
    And I click on the Assign Alternative Help icon
    Then a Missing Information validation message is displayed to the user

# Assign a case to a specialist provider.
@complete_case
Scenario: Attempt to assign a complete case
    Given I select to 'Create a case'
    And I enter the case notes "All is okay with this case"
    And I have created a user
    And I have created a valid discrimination scope
    And I am on the Diversity tab
    When I select 'Prefer not say' for all diversity questions
    And select the Assign tab
    When I select a category from Matter Type 1
    And I select a category from Matter Type 2
    And there is only one provider
    And I select 'Assign Provider'
    Then the case is assigned to the Specialist Provider
    And I am on the 'call centre dashboard' page
    And the case does not show up on the call centre dashboard

@complete_case_ooh
Scenario: Attempt to assign a complete case out of hours
    Given I select to 'Create a case'
    And I enter the case notes "All is okay with this case"
    And I have created a user
    And I have created a valid discrimination scope
    And I am on the Diversity tab
    When I select 'Prefer not say' for all diversity questions
    And select the Assign tab
    When I select a category from Matter Type 1
    And I select a category from Matter Type 2
    And I choose a provider
    And I select 'Assign Provider'
    Then the case is assigned to the Specialist Provider
    And I am on the 'call centre dashboard' page
    And the case does not show up on the call centre dashboard

@incomplete_case
Scenario: Attempt to assign an incomplete case
    Given I select to 'Create a case'
    And case notes are empty
    And I have created a user
    And I have created a valid discrimination scope
    And I am on the Diversity tab
    When I select 'Prefer not say' for all diversity questions
    And select the Assign tab
    Then I get a message with the text "Case notes must be added to close a case"

# Assign face to face.
# Journey P6, LGA-1831
@assign_f2f
Scenario: Assign face to face checking survey reminder
    Given I am on the Alternative Help page
    When I enter "the FALA search results" in the Assignment comments box
    Then I can select the Assign F2F button
    And I am shown the survey reminder
    And select continue on the survey reminder
    Then I am taken to the "Cases" page located on "/call_centre/"

# Give a decision for various diagnosis journeys
# Confirms that get INSCOPE or OUTOFSCOPE as required
@in_scope_debt_court
Scenario: Given an INSCOPE decision when selecting debt and court proceedings
    Given I am on the 'call centre dashboard' page
    And I select to 'Create a case'
    And a client with an existing case is added to it
    When I select ‘Create Scope Diagnosis'
    And I select the diagnosis <category> and click next <number> times
        | category                                                | number |
        | Debt and housing - loss of home                         | 1      |
        | Homeless or at risk of becoming homeless within 56 days | 1      |
        | A court has issued possession proceedings               | 1      |
    And I get an "INSCOPE" decision
    And select the "Create financial assessment" button
    Then I am taken to the "Finances" tab with the ‘Details’ sub-tab preselected
    #This is the icon in the top RH corner
    When I click on the Assign Alternative Help icon
    Then I am taken to the "Alternative help" page for the case located at "/alternative_help/"
    Then I select the "Housing" knowledge base category
    And I select the alternative help organisations "Housing Ombudsman - Housing Ombudsman"
    And I select the alternative help organisations "Shelter Adviceline - Shelter Adviceline"
    And I enter "This client needs housing help" in the Assignment comments box
    #This is the button on the bottom of the page
    And I click the Assign Alternative Help button
    And I am shown the survey reminder
    And select continue on the survey reminder
    And I am on the 'call centre dashboard' page

@inscope_discrim_disability
Scenario: Given an INSCOPE decision when selecting discrimination at work
    Given I select to 'Create a case'
    When I select ‘Create Scope Diagnosis'
    And I select the diagnosis <category> and click next <number> times
        | category                                                | number |
        | Discrimination                                          | 2      |
        | Direct discrimination                                   | 1      |
        | Disability                                              | 1      |
        | Work                                                    | 1      |
    Then I get an "INSCOPE" decision
    And select the "Create financial assessment" button
    Then I am taken to the "Finances" tab with the ‘Details’ sub-tab preselected

@inscope_family_skip_financial_assessment
Scenario: Skip means assessment when parent seeking to discharge Special Guardianship order
    Given I select to 'Create a case'
    And I select ‘Create Scope Diagnosis'
    When I select the "Family" option and click next
    And I select the "Special Guardianship Order" option and click next
    And I select the "parent" option and click next
    Then I get an "INSCOPE" decision
    And select the "Skip financial assessment" button
    And I remain in the "Scope" tab

@inscope_family_complete_financial_assessment
Scenario: Move on to means assessment when other person seeking to discharge Special Guardianship order
    Given I select to 'Create a case'
    And I select ‘Create Scope Diagnosis'
    When I select the "Family" option and click next
    And I select the "Special Guardianship Order" option and click next
    And I select the "other person" option and click next
    Then I get an "INSCOPE" decision
    And select the "Create financial assessment" button
    And I am taken to the "Finances" tab with the ‘Details’ sub-tab preselected
