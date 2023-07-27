@cla_frontend
Feature: Editing means test assessment as a specialist provider
  Confirming a specialist provider

  Background: Login
    Given I am logged in as "TEST_SPECIALIST_PROVIDER"

#  We were going into a case that already exists and changing 500 to 500500 for some reason
#  amended step "I <answer> to Finances <question> to
#  clear the text field and then send keys instead of appending to the end of a string
  @specialist-provider-edit-case
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
    #When I select Finances
    #And I move onto Finances inner-tab
    #And I can see on Finances inner-tab that the values remain updated
    #  | question                                             | answer |
    #  | How much was in your bank account/building           | 500.00 |
    #  | Do you have any investments, shares or ISAs?         | 0.00   |
    #  | Do you have any valuable items worth over £500 each? | 0.00   |
    #  | Do you have any money owed to you?                   | 0.00   |


