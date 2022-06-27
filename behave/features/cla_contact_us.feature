 Feature: Contact us link
     As a CLA/FALA developer, I want to test the contact us journey,
     so that I can complete the e2e test journey.

 Background: Start page
     Given I have selected the start now button on the start page

# Journey P9, Tickets combined (LGA-1874,LGA-2106)
@cla-contact-us-link-journey
Scenario: contact us journey to contact civil legal advice page / form
    Given I select 'Contact us' from the banner
    And I select <question> from the contact civil legal advice page
      | question                       |
      | I’d prefer to speak to someone |
    And I click 'continue to contact CLA'
    And I am taken to the "Contact Civil Legal Advice" page located on "/contact"
    Then I enter a name in the 'Your full name' field
    And I select the contact option 'I’ll call CLA'
    And I select 'Submit details'
    Then I am taken to the "Your details have been submitted" page located on "/result/confirmation"
