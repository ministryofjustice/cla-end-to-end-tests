Feature: Out of scope means tests

Background: Start page
    Given I have selected the start now button on the start page

@cla-out-of-scope-family-divorce
Scenario: Complete out of scope means test for family and divorce
    Given I am taken to the "Choose the area you most need help with" page located on "/scope/diagnosis/"
    When I select the category <category>
        | category                                                        |
        | Family                                                          |
        | Divorce, separation or dissolution                              |
        | Any other problem to do with divorce, separation or dissolution |
    Then I am taken to the "Legal aid doesn’t cover all types of problem" page located on "/scope/refer/family"