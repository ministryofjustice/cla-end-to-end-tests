Feature: User journeys for Fox admin or cla_backend

Background: Start page
    Given I am logged in as "CHS_GENERAL_USER"
    And I have created cases with callbacks
    Then I am logged in as "FOX_ADMIN_GENERAL_USER"

#Journey P10  Navigate to reports page and download MI callback report (LGA-1860, LGA-1861)
@fox-csv
Scenario: Navigate to reports page and download MI callback report
Given I select the link "MI CB1 Extract"
And I am taken to the "MI CB1 Extract" page located on "/admin/reports/mi-cb1-extract/"
When I enter a date range
And I select 'Export'
And the report is processed and available to download as a .csv
Then I download the .csv
And I select the link "Log out"
