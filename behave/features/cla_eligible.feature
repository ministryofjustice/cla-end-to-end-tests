Feature: In scope means tests and some with callback or confirmation details after successful means test

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
  And The callback should have been created on the CHS

@cla-in-scope-contact
Scenario: Complete callback form
  Given I have passed the means test
  And I enter my personal details
  And I select the the callback option to callback CLA
  # All steps that are clicking continue written in identical format so can reuse code
  And I click continue
  Then I am taken to the "Your details have been submitted" page located on "/result/confirmation"
  And I should be shown the CLA number
  And I should see my reference number after the text "Your reference number is"
  And A matching case should be created on the CHS

#Journey P8 Test the Housing category in scope journey. (LGA-1816)
@cla-in-scope-housing
Scenario: Complete in scope housing check
  Given I am taken to the "Choose the area you most need help with" page located on "/scope/diagnosis/"
  When I select the category <category>
     | category                              |
     | Housing                               |
     | You’re living in rented accommodation |
     | Eviction                              |
  Then I am taken to the "Legal aid is available for this type of problem" page located on "/legal-aid-available"

