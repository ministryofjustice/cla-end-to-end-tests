@cla_public
Feature:
  - In scope means tests and some with callback or confirmation details after successful means test
  - Out of scope means tests

Background: Start page
    Given I have selected the start now button on the start page

@cla-in-scope-callback, @a11y-check
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

@cla-in-scope-contact, @a11y-check
Scenario: Complete callback form
  Given I have passed the means test
  And I enter my personal details
  And I select the contact option 'I’ll call CLA'
  # All steps that are clicking continue written in identical format so can reuse code
  And I click continue
  Then I am taken to the "Your details have been submitted" page located on "/result/confirmation"
  And I should be shown the CLA number
  And I should see my reference number after the text "Your reference number is"
  And A matching case should be created on the CHS

#Journey P8  Housing category in scope journey but fail means test. (LGA-1816, LGA-1819)
@cla-in-scope-fail-financially-housing, @a11y-check
Scenario: Complete in scope housing check
  Given I am taken to the "Choose the area you most need help with" page located on "/scope/diagnosis/"
  When I select the category <category>
     | category                              |
     | Housing                               |
     | You’re living in rented accommodation |
     | Eviction                              |
  Then I am taken to the "Legal aid is available for this type of problem" page located on "/legal-aid-available"
  And I click on the 'Check if you qualify financially' button
  And I am taken to the "About you" page located on "/about"
  And I <answer> the <question>
     | question                                                   | answer |
     | Do you have a partner?                                     | No     |
     | Do you receive any benefits (including Child Benefit)?     | No     |
     | Do you have any children aged 15 or under?                 | No     |
     | Do you have any dependants aged 16 or over?                | No     |
     | Do you own any property?                                   | Yes    |
     | Are you employed?                                          | No     |
     | Are you self-employed?                                     | No     |
     | Are you or your partner (if you have one) aged 60 or over? | No     |
     | Do you have any savings or investments?                    | No     |
     | Do you have any valuable items worth over £500 each?       | No     |
  And I click continue
  And I am taken to the "Your property" page located on "/property"
  And I <answer> the <question>
     | question                                                   | answer |
     | Is this property your main home?                           | No     |
     | Does anyone else own a share of the property?              | No     |
     | How much is the property worth?                            | 50000  |
     | How much is left to pay on the mortgage?                   | 0      |
     | How much was your monthly mortgage repayment last month?   | 0      |
     | Do you rent out any part of this property?                 | No     |
     | Is your share of the property in dispute?                  | No     |
  And I click continue
  And I am taken to the "Review your answers" page located on "/review"
  And I click Confirm
  And I am taken to the "You’re unlikely to get legal aid" page located on "/result/refer/housing"

# Out of scope means tests
@cla-out-of-scope-family-divorce, @a11y-check
Scenario: Complete out of scope means test for family and divorce
  Given I am taken to the "Choose the area you most need help with" page located on "/scope/diagnosis/"
  When I select the category <category>
    | category                                                        |
    | Family                                                          |
    | Divorce, separation or dissolution                              |
    | Any other problem to do with divorce, separation or dissolution |
  Then I am taken to the "Legal aid doesn’t cover all types of problem" page located on "/scope/refer/family"

