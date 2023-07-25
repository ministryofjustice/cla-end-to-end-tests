@cla_frontend
Feature: - Testing the complaints dashboard

#Redirects to OOH URL for frontend OOH tests
Background: Login
    Given I am logged in as "CHS_MANAGER_USER"

@complaints
Scenario: Search for a complaint
    Given I am on the 'Complaints' tab on the dashboard
    And There are cases available
    When I search for 'JT-4272-9443'
    And The complaint i search for is available
    And I select the complaint 'JT-4272-9443'
    And I am on the complaint 'JT-4272-9443'

@complaints
Scenario: Search for a complaint failure
    Given I am on the 'Complaints' tab on the dashboard
    And There are cases available
    When I search for 'Failing'
    And The complaint i search for is not available