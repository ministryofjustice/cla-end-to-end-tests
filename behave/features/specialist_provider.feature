Feature: Specialist Provider Case Assignment

Background: Log In Provider
    Given that I am logged in
    And I select to 'Create a case'
    And I enter the case notes "All is okay with this case"
    And I have created a user
    And I have created a valid discrimination scope
    And I am on the Diversity tab
    When I select 'Prefer not say' for all diversity questions
    And select the Assign tab
    When I select a category from Matter Type 1
    And I select a category from Matter Type 2
    # And there is only one provider
    # And I choose "Howells" as Specialist Provider
    # And I select 'Assign Provider'
    # # And I log out
    And I am logged in as a Specialist Provider
 
@specialist-provider-select-case
Scenario: Specialist Provider Selects a case
  Given that I am on the specialist provider cases dashboard page
  # And there is a case available
#   When I select a case from the dashboard
#   Then I am taken to the case details page
  