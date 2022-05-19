Feature: Select Callbacks for Digital Cases
# Looking at the callbacks calendar view to see whether callbacks have been created and then viewing the cases

#As a CHS Operator, I want to select a callback slot, so I can see the cases where a callback is booked for that slot.
Background: Create Callbacks
    Given that I am logged in

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


