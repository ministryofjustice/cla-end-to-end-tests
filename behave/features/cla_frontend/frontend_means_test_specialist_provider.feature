@cla_frontend
Feature: Editing means test assessment as a specialist provider
  Confirming a specialist provider

  Background: Login
    Given I am logged in as "TEST_SPECIALIST_PROVIDER"

  @specialist-provider-edit-case
  Scenario: Specialist Provider Edits a case
    Given I am on the specialist provider cases dashboard page
    And there is a case available
    And I select a case to accept from the dashboard
    And I am taken to the "specialist provider" case details page
    When I select Finances
    And I move onto Finances inner-tab
  #need to make sure we are actually changing a value here and still eligible when we do it
    And I <answer> to Finances <question>
      | question                                             | answer |
      | How much was in your bank account/building           | 500.00 |
      | Do you have any investments, shares or ISAs?         | 0.00   |
      | Do you have any valuable items worth over £500 each? | 0.00   |
      | Do you have any money owed to you?                   | 0.00   |
    And I select Save assessment
 # step checking the messages at the side?   `Then I can see my accepted case reference number`
    When I return to the specialist provider cases dashboard page

    And there is a case available
    And I select a case to accept from the dashboard
    And I am taken to the "specialist provider" case details page
    When I select Finances
    And I move onto Finances inner-tab
#  And The legal help form "Your Finances" section has the values
    And I can see on Finances inner-tab that the values remain updated
      | question                                             | answer |
      | How much was in your bank account/building           | 500.00 |
      | Do you have any investments, shares or ISAs?         | 0.00   |
      | Do you have any valuable items worth over £500 each? | 0.00   |
      | Do you have any money owed to you?                   | 0.00   |
# And I can view my changed <answer> to Finances <question>


