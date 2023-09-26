@cla_backend
Feature: Security checks to ensure CLA_Backend timesouts

Background: Log in to the Fox admin as a user within the super users group
    Given I am logged in as "FOX_ADMIN_SECURITY_USER"

@security @inactivity
Scenario: After a set period of time, CLA Backend should timeout from inactivity
    Given The session warning is not visible
    And I wait for the session warning
    And I wait for the page to timeout
    Then I am logged out

@security @inactivity @passive-url
Scenario: Confirm that the session times out on passive urls
    Given I am on a passive URL
    And The session warning is not visible
    And I wait for the session warning
    And I wait for the page to timeout
    Then I am logged out

@security @session-end
Scenario: Confirm that the session ends on browser close
    Then I have a session cookie that has no expiry