@cla_frontend
Feature: - Check additional question under the ‘immigration and asylum’ scope.

  Background: Login
    Given I am logged in as "CHS_GENERAL_USER"

  @referred_by_provider_south_west
  Scenario: Case has been referred by a provider in the south west of england.
    Given I select to 'Create a case'
    And I select ‘Create Scope Diagnosis'
    When I select the "Immigration and asylum" option and click next
    And I select the "any other matter - immigration" option and click next
    And I select the "client was referred to CLA by a provider" option and click next
    And I select the "Refer the client to the alternative list" option and click next
    Then I get an "OUTOFSCOPE" decision

  @referred_through_any_other_route
  Scenario: Case has been referred through any other route.
    Given I select to 'Create a case'
    And I select ‘Create Scope Diagnosis'
    When I select the "Immigration and asylum" option and click next
    And I select the "any other matter - immigration" option and click next
    And I select the "client came to CLA through any other route" option and click next
    And I select the "Refer the client to FALA" option and click next
    Then I get an "OUTOFSCOPE" decision

  @referred_through_any_other_route
  Scenario: Check South West England help text appears
    Given I select to 'Create a case'
    And I select ‘Create Scope Diagnosis'
    When I select the "Immigration and asylum" option and click next
    And I select the "any other matter - immigration" option and click next
    And I click the help button on to the "any other matter - immigration" option
    Then the help text for "any other matter - immigration" is:
    """
    South West of England consists of the counties of Cornwall (including the Isles of Scilly),
     Dorset, Devon, Gloucestershire, Somerset and Wiltshire
    """
