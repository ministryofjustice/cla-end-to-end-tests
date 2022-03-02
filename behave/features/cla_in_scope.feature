Feature: In scope outcome

Background: Start page
    Given I have selected the start now button on the start page

@cla-in-scope
Scenario: Select the in scope special education needs category
    # All steps that are just checking a page exists written in identical format so can reuse code
    Given I am taken to the "Choose the area you most need help with" page located on "/scope/diagnosis/"
    When I select the category Education
    And the category Special Educational needs
    Then I am taken to the "Legal aid is available for this type of problem" page located on "/legal-aid-available"
    And I click on the 'Check if you qualify financially' button 
    And I am taken to the "About you" page located on "/about"