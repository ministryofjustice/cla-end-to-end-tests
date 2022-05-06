Feature: Create and start case callbacks.
    Create callbacks for cla public cases
    Start pending callbacks
    Remove started callbacks

Background: Login
    Given that I am logged in

@said-wip-callback
Scenario: Start callback
  GIVEN that I am viewing the case "7Y-6712-2429" which has a callback
#  WHEN I select "Start Call"
#  THEN the call has started
#  AND I remove the callback
  THEN this case is removed from callback list (calendar view)