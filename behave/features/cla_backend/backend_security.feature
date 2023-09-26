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

@security @sessionend
Scenario: Confirm that the session ends on browser close
    Given I close the browser
    And I open a new CHS browser
    Then I am logged out

    
@security @inactivity @passiveurl
Scenario: Confirm that the session timesout on passive urls
    Given I am on a passive URL
    And The session warning is not visible
    And And I wait for the session warning
    And I wait for the page to timeout
    Then I am logged out



