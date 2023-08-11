@cla_frontend
Feature: Editing means test assessment as a specialist provider
  Confirming a specialist provider

# Background will fail if not between DISCRIMINATION_START_TIME_HR and DISCRIMINATION_END_TIME_HR
  Background: Login
    Given I am logged in as "TEST_SPECIALIST_PROVIDER"


  @specialist-provider-edit-case
  Scenario: Specialist Provider Edits a case
    Given I am on the specialist provider cases dashboard page
    And I select a "CLA_SPECIALIST_CASE_TO_EDIT" case from the dashboard
    And I am taken to the "specialist provider" case details page
    And I select Finances
    And I move onto Finances inner-tab
    And I <answer> to Finances <question>
      | question                                             | answer |
      | How much was in your bank account/building           | 500    |
      | Do you have any investments, shares or ISAs?         | 0.00   |
      | Do you have any valuable items worth over £500 each? | 0.00   |
      | Do you have any money owed to you?                   | 0.00   |
    When I select Save assessment
    And I am given a message 'The means test has been saved. The current result is eligible for Legal Aid'
    And I return to the specialist provider cases dashboard page
    And I select a "CLA_SPECIALIST_CASE_TO_EDIT" case from the dashboard
    And I am taken to the "specialist provider" case details page
    And I select Finances
    And I move onto Finances inner-tab
    Then I can see on Finances inner-tab <question> that the <answer> remain updated
      | question                                             | answer |
      | How much was in your bank account/building           | 500    |
      | Do you have any investments, shares or ISAs?         | 0.00   |
      | Do you have any valuable items worth over £500 each? | 0.00   |
      | Do you have any money owed to you?                   | 0.00   |