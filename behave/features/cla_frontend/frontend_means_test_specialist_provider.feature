@cla_frontend
Feature: Editing means test assessment as a specialist provider
  Confirming a specialist provider

# Background will fail if not between DISCRIMINATION_START_TIME_HR and DISCRIMINATION_END_TIME_HR
  Background: Login
    Given I am logged in as "CHS_GENERAL_USER"
    And I select to 'Create a case' for editing
    Then I enter the case notes "I am creating this case to edit it"
    And I complete the users details with EDIT details
    When I have created a valid discrimination scope
    And I am on the Diversity tab having answered the finances questions
    Then I select 'Prefer not say' for all diversity questions
    And I select the Assign tab
    Then I select a category from Matter Type 1
    And I select a category from Matter Type 2
    Then I select the "Assign manually" button
    And I choose a provider
    And I select 'Assign Provider'
    Then the case is assigned to the Specialist Provider
    Then I select the 'Sign out' link
    And I am logged in as "TEST_SPECIALIST_PROVIDER"


  @specialist-provider-edit-case
# The case in use has been created previously in the background
# Howells selects that case, edits it and come back to verify that the values remain the same
  Scenario: Specialist Provider Edits a case
    Given I am on the specialist provider cases dashboard page
    And I select a case to edit from the dashboard
    And I am taken to the "specialist provider" case details page
    When I select Finances
    And I move onto Finances inner-tab
    And I <answer> to Finances <question>
      | question                                             | answer |
      | How much was in your bank account/building           | 500    |
      | Do you have any investments, shares or ISAs?         | 0.00   |
      | Do you have any valuable items worth over £500 each? | 0.00   |
      | Do you have any money owed to you?                   | 0.00   |
    And I select Save assessment
    Then I am given a message 'The means test has been saved. The current result is eligible for Legal Aid'
    When I return to the specialist provider cases dashboard page
    And I select a case to edit from the dashboard
    And I am taken to the "specialist provider" case details page
    When I select Finances
    And I move onto Finances inner-tab
    And I can see on Finances inner-tab <question> that the <answer> remain updated
      | question                                             | answer |
      | How much was in your bank account/building           | 500    |
      | Do you have any investments, shares or ISAs?         | 0.00   |
      | Do you have any valuable items worth over £500 each? | 0.00   |
      | Do you have any money owed to you?                   | 0.00   |