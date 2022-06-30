Feature: User journeys for Fox admin or cla_backend

Background: Start page
    Given that I am logged in as "FOX_ADMIN_GENERAL_USER"

#Journey P10  Navigate to reports page and download MI callback report (LGA-1860)
@cla-download-callback-cases-csv
Scenario: Navigate to reports page and download MI callback report
Given I select "MI CB1 Extract"
#Then I am take to the report page
