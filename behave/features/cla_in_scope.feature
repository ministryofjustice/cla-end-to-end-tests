Feature: In scope outcome

Background: Start page
    Given I have selected the start now button on the start page

@cla-in-scope
Scenario: Select the in scope special education needs category
    Given I am on the scope diagnosis page
    When I select the category Education
    And the category Special Educational needs
    Then I am taken to the Legal aid is available for this type of problem page