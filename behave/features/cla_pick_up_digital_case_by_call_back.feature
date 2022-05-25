Feature: Check Callbacks for Digital Cases
# Looking at the callbacks calendar view to see whether callbacks have been created and then viewing the cases

#As a CHS Operator, I want to select a callback slot, so I can see the cases where a callback is booked for that slot.
Background: Create Callbacks
    Given that I am logged in
    And that I have created cases with callbacks


@check_callback_exists
Scenario: Can see callbacks booked in different slots
    Given that I am on cases callback page
    And multiple cases with a callback exists
    When I select a callback slot
    Then I can see the cases where a callback is booked for that slot