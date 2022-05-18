Feature: Check Callbacks for Digital Cases
# Looking at the callbacks calendar view to see whether callbacks have been created and then viewing the cases

#As a CHS Operator, I want to select a callback slot, so I can see the cases where a callback is booked for that slot.
Background: Create Callbacks
    Given that I am logged in

@view_existing_callback
Scenario: Can see details of selected callback
    Given I am viewing a callback slot
    And callback slot contains a case created on CLA Public
    When I select a case created on CLA Public from the callback slot
    #Then I should be taken to the case details page
    #And I should see the clients email address, name, address, telephone and the case source should be set to web

