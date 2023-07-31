@cla_frontend
Feature: Under 18 Changes
    Confirming if a person who is 18 and under is eligible or not

Background: Login
    Given I am logged in as "CHS_GENERAL_USER"

@above_18_no_follow_up_questions
Scenario: Person aged 18 and above does not answer the follow up under 17 questions
    Given I select to 'Create a case'
    And I am on the Finances tab with the ‘Details’ sub-tab preselected
    When I am not aged 17 or under
    Then I can not answer the following 17 or under questions

@under_18_receives_money_regularly
Scenario: Person aged under 18 receives regular payments does not receive follow up question
    Given I select to 'Create a case'
    And I am on the Finances tab with the ‘Details’ sub-tab preselected
    When I am aged 17 or under
    And I do receive money on a regular basis
    Then the do you have valuables totalling £2500 or more question does not appear
    And I select Save assessment
    And the green tick is not present in the Finance tab

@under_18_has_valuables
Scenario: Person aged under 18 with valuables over 2500 proceeds to fill means testing
    Given I select to 'Create a case'
    And I am on the Finances tab with the ‘Details’ sub-tab preselected
    When I am aged 17 or under
    And I do not receive money on a regular basis
    And I do have savings, items of value or investments totalling £2500 or more
    And I select Save assessment
    Then the green tick is not present in the Finance tab

@under_18_passported
Scenario: Person aged under 18 is passported
    Given I select to 'Create a case'
    And I am on the Finances tab with the ‘Details’ sub-tab preselected
    When I am aged 17 or under
    And I do not receive money on a regular basis
    And I do not have savings, items of value or investments totalling £2500 or more
    And I select Save assessment
    Then I am given a message 'The means test has been saved. The current result is eligible for Legal Aid'
    And the green tick is present in the Finance tab