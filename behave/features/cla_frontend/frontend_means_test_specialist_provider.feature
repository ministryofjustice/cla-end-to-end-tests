@cla_frontend
Feature: Editing means test assessment as a specialist provider
  Confirming a specialist provider

  Background: Login
    Given I am logged in as "TEST_SPECIALIST_PROVIDER"

  @specialist-provider-edit-case
  Scenario: Specialist Provider Edits a case
    Given I am on the specialist provider cases dashboard page
    And I select a case to edit from the dashboard
    And I am taken to the "specialist provider" case details page
    When I select Finances
    And I move onto Finances inner-tab
        And I <answer> to Finances <question>
      | question                                             | answer |
      | How much was in your bank account/building           | 500.00 |
      | Do you have any investments, shares or ISAs?         | 0.00   |
      | Do you have any valuable items worth over £500 each? | 0.00   |
      | Do you have any money owed to you?                   | 0.00   |
    And I select Save assessment
  #need to make sure we are actually changing a value here and still eligible when we do it
  # step here checking the messages at the side?   `Then I can see my accepted case reference number`
  # this step fails with the following error:
  # selenium.common.exceptions.ElementClickInterceptedException: Message: element click intercepted: Element <a ui-sref="case_list(caseListStateParams)" class="SubNav-link SubNav-link--back" href="/provider/">...</a> is not clickable at point (134, 20). Other element would receive the click: <a ui-sref="case_detail.edit.diagnosis" class="ng-binding" href="/provider/JT-4272-9443/diagnosis/">...</a>
       # (Session info: chrome=112.0.5615.165)

    #When I return to the specialist provider cases dashboard page
    #And I select a case to edit from the dashboard
    #And I am taken to the "specialist provider" case details page
    #When I select Finances
    #And I move onto Finances inner-tab
    #And I can see on Finances inner-tab that the values remain updated
    #  | question                                             | answer |
    #  | How much was in your bank account/building           | 500.00 |
    #  | Do you have any investments, shares or ISAs?         | 0.00   |
    #  | Do you have any valuable items worth over £500 each? | 0.00   |
    #  | Do you have any money owed to you?                   | 0.00   |


