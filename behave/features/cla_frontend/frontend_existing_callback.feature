@cla_frontend
Feature: Check Callbacks for Digital Cases
# Looking at the callbacks calendar view to see whether callbacks have been created and then viewing the cases

#As a CHS Operator, I want to select a callback slot, so I can see the cases where a callback is booked for that slot.
Background: Create Callbacks
    Given I am logged in as "CHS_GENERAL_USER"
    And I have created cases with callbacks


@check_callback_exists
Scenario: Can see callbacks booked in different slots
    Given that I am on cases callback page
    And multiple cases with a callback exists
    When I select a callback slot
    Then I can see the cases where a callback is booked for that slot


@view_existing_callback
Scenario: Can see details of selected callback
    Given I am viewing a callback slot
    And callback slot contains a case created on CLA Public
    When I select a case created on CLA Public from the callback slot
    Then I am taken to the "call centre" case details page
    And I can view the client details of a case created on CLA Public
        | details     |
        | Full name   |
        | Telephone   |
    When I select "Start Call"
    Then the call has started
    And I remove the callback
    Then this case is removed from callback list (calendar view)