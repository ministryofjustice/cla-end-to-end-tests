Feature: Correct decision on discrimination diagnosis.
    Confirms that when a case with the scope diagnosis of 'discrimination,
    direct discrimination, disability, work' is selected that you
    get an INSCOPE decision.

Background: Login
    Given that I am logged in

Scenario: Given an INSCOPE decision when selecting discrimination at work
    Given I select to 'Create a case'
    When I select ‘Create Scope Diagnosis'
    And I select the categories Discrimination, Direct Discrimination, Disability, Work
    Then I get an INSCOPE decision
    And select 'Create financial assessment'
    Then I am taken to the Finances tab with the ‘Details’ sub-tab preselected