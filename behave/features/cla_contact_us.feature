 Feature: Contact us link
     As a CLA/FALA developer, I want to test the contact us journey,
     so that I can complete the e2e test journey.

 Background: Start page
     Given I have selected the start now button on the start page

@cla-contact-us-link
Scenario: contact us journey to contact civil legal advice page / form
    Given I select 'Contact us' from the banner
    And I select <question> from the contact civil legal advice page
      | question                       |
      | I’d prefer to speak to someone |
    And I click 'continue to contact CLA'
    Then I am taken to the 'contact civil legal advice' page
