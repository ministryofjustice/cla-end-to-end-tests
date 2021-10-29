
Feature: Assign incomplete case.
    Confirms that case notes are needed before assigning
    a case.

Background: Login
    Given that I am logged in
@wip
Scenario: Attempt to assign an incomplete case
    Given I select to 'Create a case'
    And case notes are empty
    And I am on the Diversity tab
    When I select 'Prefer not say' for all diversity questions
    And select the Assign tab
    Then I get a message with the text "Case notes must be added to close a case"