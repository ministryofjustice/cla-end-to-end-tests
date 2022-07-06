Feature: Assign a case to a specialist provider.

Background: Login
    Given that I am logged in as "CHS_GENERAL_USER"

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