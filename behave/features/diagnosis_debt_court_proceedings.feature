Feature: Correct decision on debt and court proceedings.
    Confirms that when a case with the scope diagnosis of 'Debt and housing - loss of home,
    Homeless or at risk of becoming homeless within 56 days, A court has issued possession proceedings' is selected that you
    get an INSCOPE decision.
    This scenario will reuse lots of the steps from the discrimination diagnosis P1 cases

Background: Login
    Given that I am logged in

@in_scope_debt_court
Scenario: Given an INSCOPE decision when selecting debt and court proceedings
    Given I am taken to the "call centre" case details page
    And a client with an existing case is added to it
    When I select ‘Create Scope Diagnosis'
    And I select the diagnosis <category> and click next <number> times
        | category                                                | number |
        | Debt and housing - loss of home                         | 1      |
        | Homeless or at risk of becoming homeless within 56 days | 1      |
        | A court has issued possession proceedings               | 1      |
    Then I get an INSCOPE decision
    And select 'Create financial assessment'
    Then I am taken to the Finances tab with the ‘Details’ sub-tab preselected