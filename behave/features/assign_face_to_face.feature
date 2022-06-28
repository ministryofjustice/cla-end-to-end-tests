Feature: Assign face to face.
    As a CHS operator, I need the ability to complete 
    the face to face assignment, so that I can populate 
    the survey and complete the end to end testing.

Background: Login
    Given that I am logged in

@wip
Scenario: Assign face to face checking survey reminder
    Given that I am on the Alternative Help page
    When I enter "the FALA search results" in the Assignment comments box
    Then I am can select Assign F2F button
    And I am shown the survey reminder
    And select continue on the the survey reminder
    Then I am taken to the call centre dashboard page