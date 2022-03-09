Feature: Complete callback details after successful means test

Background: Start page
    Given I have selected the start now button on the start page
    
@cla-in-scope-callback
Scenario: Complete callback form asking for callback
  Given I have passed the means test
  And I enter my personal details
  And I select "Call me back"
  And I enter my phone number for the callback
  And I select "Call on another day"
  And I select an available day and time
  # # All steps that are clicking continue written in identical format so can reuse code
  And I click continue
  Then I am taken to the "We will call you back" page located on "/result/confirmation"
  And I should NOT see the text "You can now call CLA on 0345 345 4 345"
  And I should see my reference number after the text "Your reference number is"
  And A matching case should be created on the CHS
  And The callback should have been created
