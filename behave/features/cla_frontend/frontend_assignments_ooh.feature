@cla_frontend @ooh
Feature: - Assign alternative help to out of scope case.
         - Assign a case to a specialist provider.
         - Assign face to face.
         - Diagnosis diagnosis journeys

#Redirects to OOH URL for frontend OOH tests
Background: Login
    Given I am logged in as "CHS_GENERAL_USER_OOH"

# Test will fail if run between DISCRIMINATION_START_TIME_HR and DISCRIMINATION_END_TIME_HR
@complete_case_ooh @ooh
Scenario: Attempt to assign a complete case out of hours
    Given I select to 'Create a case'
    And I enter the case notes "All is okay with this case"
    And I have created a user
    And I have created a valid discrimination scope
    And I am on the Diversity tab having answered the finances questions
    When I select 'Prefer not say' for all diversity questions
    And I select the Assign tab
    When I select a category from Matter Type 1
    And I select a category from Matter Type 2
    And I choose a provider
    And I select 'Assign Provider'
    Then the case is assigned to the Specialist Provider
    And I am on the 'call centre dashboard' page
    And the case does not show up on the call centre dashboard ooh