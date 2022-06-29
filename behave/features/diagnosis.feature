Feature: Give a decision for various diagnosis journeys
Confirms that get INSCOPE or OUTOFSCOPE as required

Background: Login
    Given that I am logged in

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
    And select 'Create financial assessment'
    Then I am taken to the Finances tab with the ‘Details’ sub-tab preselected
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
    And select 'Create financial assessment'
    Then I am taken to the Finances tab with the ‘Details’ sub-tab preselected