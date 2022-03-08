Feature: Complete callback details after successful means test

Background: Start page
    Given I have selected the start now button on the start page
    
@cla-in-scope--contact
Scenario: Complete callback form
  Given I have passed the means test
#  And I am on the financially eligible outcome page located at /result/eligible
  And I enter "John Smith" as my full name
  And I enter "test@civillegaladvice.service.gov.uk" as my email address
  And I enter "SW1H 9AJ" as my postcode
  And I enter "105 Petty France" street address
  And I select the the callback option to callback CLA
  And click "Submit details"
  Then I should be taken to the "Your details have been submitted" page
  And I should shown the CLA number
  And I should see my reference number after the text "Your reference number is"
  And A matching case should be created on the CHS
