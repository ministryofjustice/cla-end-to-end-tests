Feature: Smoke test
  As a developer,
  I want to check that the frontend and backend services are up,
  So that I know I can run tests on them.

  Scenario: Cla backend check
    Given I go to the "cla backend" status endpoint
    Then I am shown that the "cla backend" service is ready

  Scenario: Cla frontend check
    Given I go to the "cla frontend" status endpoint
    Then I am shown that the "cla frontend" service is ready

  Scenario: Cla public check
    Given I go to the "cla public" status endpoint
    Then I am shown that the "cla public" service is ready