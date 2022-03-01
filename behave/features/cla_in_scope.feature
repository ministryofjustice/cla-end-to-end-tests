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
    And I <answer> the <question> 
        | question                                                   | answer |
        | Do you have a partner?                                     | No     |
        | Do you receive any benefits (including Child Benefit)?     | Yes    |
        | Do you have any children aged 15 or under?                 | No     |
        | Do you have any dependants aged 16 or over?                | No     |
        | Do you own any property?                                   | No     |
        | Are you employed?                                          | No     |
        | Are you self-employed?                                     | No     |
        | Are you or your partner (if you have one) aged 60 or over? | No     |
        | Do you have any savings or investments?                    | No     |
        | Do you have any valuable items worth over £500 each?       | No     |
    # All steps that are clicking continue written in identical format so can reuse code
    And I click continue
    And I am taken to the "Which benefits do you receive?" page located on "/benefits"
    And I select 'Universal Credit' from the list of benefits
    And I click continue 
    And I am taken to the "Review your answers" page located on "/review"
    # this is actually click confirm. Submit button has text confirm on it but same details as continue buttons
    And I click continue
    Then I am taken to the "Contact Civil Legal Advice" page located on "/result/eligible"