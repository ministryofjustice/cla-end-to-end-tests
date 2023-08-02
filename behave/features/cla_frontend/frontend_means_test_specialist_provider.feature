@cla_frontend
Feature: Editing means test assessment as a specialist provider
  Confirming a specialist provider

  Background: Login
    Given I am logged in as "CHS_GENERAL_USER"
     Given I select to 'Create a case'
    And I enter the case notes "All is okay with this case"
    And a client with an existing case is added to it
    And I have created a valid discrimination scope
    Given I am taken to the "Finances" tab with the ‘Details’ sub-tab preselected
        And I do not have a partner
        And I am aged 60 or over
        And I <answer> to Details <question>
          | question                                          | answer |
          | Universal credit                                  | No     |
          | Income Support                                    | No     |
          | Income-based Job Seekers Allowance                | No     |
          | Guarantee State Pension Credit                    | Yes    |
          | Income-related Employment and Support Allowance   | No     |
        Then I move onto Finances inner-tab
        And I <answer> to Finances <question>
          | question                                              | answer |
          | How much was in your bank account/building society    | 0.00   |
          | Do you have any investments, shares or ISAs?          | 0.00   |
          | Do you have any valuable items worth over £500 each?  | 0.00   |
          | Do you have any money owed to you?                    | 0.00   |
        And I select Save assessment
        And the 'Diversity' and 'Assign' tabs become available
    And I fill in the Diversity tab if I need to
    And select the Assign tab
    When I select a category from Matter Type 1
    And I select a category from Matter Type 2
    And there is only one provider
    And I select 'Assign Provider'
    Then the case is assigned to the Specialist Provider
    And I have created a case to edit in hours
    And I select the link "Log out"
    Then I am logged in as "TEST_SPECIALIST_PROVIDER"

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
    When I select Finances
    And I move onto Finances inner-tab
    And I can see on Finances inner-tab <question> that the <answer> remain updated
      | question                                             | answer |
      | How much was in your bank account/building           | 500    |
      | Do you have any investments, shares or ISAs?         | 0.00   |
      | Do you have any valuable items worth over £500 each? | 0.00   |
      | Do you have any money owed to you?                   | 0.00   |


