 Feature: Contact us link
     As a CLA/FALA developer, I want to test the contact us journey,
     so that I can complete the e2e test journey.

 Background: Start page
     Given I have selected the start now button on the start page

# Journey P9, Tickets combined (LGA-1874,LGA-2106)
@cla-contact-us-link-journey, @a11y-check
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

# Journey P9, Ticket (LGA-2183)
@cla-contact-us-call-someone-else, @a11y-check
Scenario: contact us journey, selecting 'call someone else instead of me' option
  Given I am on the Contact Civil Legal Advice page
  When I enter a name in the 'Your full name' field
  And I select the contact option 'Call someone else instead of me'
  And I enter the full name of the person to call
  And I select "Family member or friend" from the 'Relationship to you' drop down options
  And I enter the phone number of the person to call back
  And I select 'Call today'
  And I select an available "thirdparty" call time
  And I select 'Submit details'
  Then I am taken to the "We will call you back" page located on "/result/confirmation"
