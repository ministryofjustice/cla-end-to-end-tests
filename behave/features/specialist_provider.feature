Feature: Specialist Provider Case Assignment
# there is now a fixture which should create two cases so that these tests can run. It is loaded by running 
# docker-compose exec clabackend python manage.py loaddata test_special_provider_case.json 
# which is in run_test_local.sh

Background: Log In Provider
    Given I am logged in as a Specialist Provider
 
# @specialist-provider-select-case
# Scenario: Specialist Provider Selects a case
#   Given that I am on the specialist provider cases dashboard page
#   And there is a case available
#   When I select a case from the dashboard
#   Then I am taken to the case details page
  
@specialist-provider-view-case-scope
Scenario: Specialist Provider Selects a case
  Given that I am on the specialist provider cases dashboard page
  And there is a case available
  And I select a case from the dashboard
  And I am taken to the case details page
  And I can view the client details
  And I can view the case details and notes entered by the Operator
  When I select Scope
  Then I can view the scope assessment entered by the Operator

@specialist-provider-accept-case
Scenario: Specialist Provider Accepts a case
  Given that I am on the specialist provider cases dashboard page
  And there is a case available
  And I select a case from the dashboard
  And I am taken to the case details page
  And I select 'Accept'
  And I can see a 'Case accepted successfully' message
  When I return to the specialist provider cases dashboard page
  And I select the Accepted tab
  Then I can see my accepted case reference number