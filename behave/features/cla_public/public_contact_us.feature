@cla_public
Feature: Contact us link
     As a CLA/FALA developer, I want to test the contact us journey,
     so that I can complete the e2e test journey.

 Background: Start page
     Given I have selected the start now button on the start page

# Journey P9, Tickets combined (LGA-1874,LGA-2106)
@cla-contact-us-link-journey @a11y-check
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
@cla-contact-us-call-someone-else @a11y-check
Scenario: contact us journey, selecting 'call someone else instead of me' option
  Given I am on the Contact Civil Legal Advice page
  When I enter a name in the 'Your full name' field
  And I select the contact option 'Call someone else instead of me'
  And I enter the full name of the person to call
  And I select "Family member or friend" from the 'Relationship to you' drop down options
  And I enter the phone number of the person to call back
  And I select the next available "thirdparty" time slot
  And I select 'Submit details'
  Then I am taken to the "We will call you back" page located on "/result/confirmation"


# Ticket (LGA-2798, LGA-2799)
@cla-contact-us-announce-cla-call @a11y-check
Scenario: contact us journey, saying 'Yes' for CLA to announce who's calling
  Given I am on the Contact Civil Legal Advice page
  When I enter a name in the 'Your full name' field
  And I select the contact option 'Call me back'
  And I enter my phone number
  And I select the next available "callback" time slot
  And I select 'Yes' to announce call options
  And I select 'Submit details'
  Then I am taken to the "We will call you back" page located on "/result/confirmation"
  And I save the reference number
  When I am logged in as "CHS_GENERAL_USER"
  When I search for and select a case using my saved reference number
  Then the 'do not announce the call is from CLA' warning is not present


@cla-contact-us-announce-cla-call @a11y-check
Scenario: contact us journey, saying 'No' for CLA to announce who's calling
  Given I am on the Contact Civil Legal Advice page
  When I enter a name in the 'Your full name' field
  And I select the contact option 'Call me back'
  And I enter my phone number
  And I select the next available "callback" time slot
  And I select 'No' to announce call options
  And I select 'Submit details'
  Then I am taken to the "We will call you back" page located on "/result/confirmation"
  And I save the reference number
  And I am logged in as "CHS_GENERAL_USER"
  And I search for and select a case using my saved reference number
  Then the 'do not announce the call is from CLA' warning is present


@cla-contact-us-announce-cla-call @a11y-check
Scenario: contact us journey, selecting 'I will call CLA'
  Given I am on the Contact Civil Legal Advice page
  When I enter a name in the 'Your full name' field
  And I select the contact option 'I will call you'
  And I select 'Submit details'
  Then I am taken to the "Your details have been submitted" page located on "/result/confirmation"
  And I save the reference number
  And I am logged in as "CHS_GENERAL_USER"
  And I search for and select a case using my saved reference number
  Then the 'do not announce the call is from CLA' warning is not present


@cla-contact-us-announce-cla-call @a11y-check
Scenario: contact us journey, selecting 'Call someone else instead of me'
  Given I am on the Contact Civil Legal Advice page
  When I enter a name in the 'Your full name' field
  And I select the contact option 'Call someone else instead of me'
  And I enter the full name of the person to call
  And I select "Family member or friend" from the 'Relationship to you' drop down options
  And I enter the phone number of the person to call back
  And I select the next available "thirdparty" time slot
  And I select 'Submit details'
  Then I am taken to the "We will call you back" page located on "/result/confirmation"
  And I save the reference number
  And I am logged in as "CHS_GENERAL_USER"
  And I search for and select a case using my saved reference number
  Then the 'do not announce the call is from CLA' warning is not present
