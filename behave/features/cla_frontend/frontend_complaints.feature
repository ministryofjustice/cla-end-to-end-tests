@cla_frontend
Feature: - Testing the complaints dashboard

#Redirects to OOH URL for frontend OOH tests
Background: Login
    Given I am logged in as "CHS_MANAGER_USER"

@complaints-search-succeeds
Scenario: Search for a complaint
    Given I am on the 'Complaints' tab on the dashboard
    And There are complaints available
    When I search for 'JT-4272-9443'
    And I can select the complaint 'JT-4272-9443'
    Then I am on the complaint 'JT-4272-9443' detail page

@complaints-search-returns-no-results
Scenario: Search for a complaint failure
    Given I am on the 'Complaints' tab on the dashboard
    And There are complaints available
    When I search for 'Failing'
    Then there are no complaints returned