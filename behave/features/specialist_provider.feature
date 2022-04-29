Feature: Specialist Provider Case Assignment
# there is now a fixture which should create two cases so that these tests can run. It is loaded by running 
# docker-compose exec clabackend python manage.py loaddata test_special_provider_case.json 
# which is in run_test_local.sh

Background: Log In Provider
    Given I am logged in as a Specialist Provider
 
# @specialist-provider-select-case
# Scenario: Specialist Provider Selects a case
#   Given that I am on the specialist provider cases dashboard page
#   And there is a case available
#   When I select a case from the dashboard
#   Then I am taken to the case details page

Scenario: Specialist Provider Selects a case
  Given that I am on the specialist provider cases dashboard page
  And there is a case available
  And I select a case from the dashboard
  And I am taken to the case details page
  And I can view the client details
  And I can view the case details and notes entered by the Operator
  When I select Scope
  Then I can view the scope assessment entered by the Operator

Scenario: Specialist Provider Accepts a case
  Given that I am on the specialist provider cases dashboard page
  And there is a case available
  And I select a case from the dashboard
  And I am taken to the case details page
  And I select 'Accept'
  And I can see a 'Case accepted successfully' message
  When I return to the specialist provider cases dashboard page
  And I select the Accepted tab
  Then I can see my accepted case reference number

@wip-said
Scenario: Specialist Provider Accepts a case
  Given that I am viewing a case that I have accepted as a specialist provider
  And I select the Legal help form
  And The legal help form Your Details section has the values
  | field                                                    | value              |
  | Full name                                                | Jo                 |
  | Our ref                                                  | 3000001            |
  | Date of Birth                                            | 1/1/2003           |
  | Surname at Birth                                         |                    |
  | Sex                                                      |                    |
  | Current Address                                          | 11 electric avenue |
  | N.I. Number                                              | NW117431B          |
  | Client No                                                |                    |
  | Post Code                                                | OX2 0LD            |
  And The legal help form "Your Finances" section has the values
  | field                                                    | value              |
  | Do you have a partner that you live with?                | No                 |
  | Universal credit                                         | Yes                |
  | Income Support                                           | No                 |
  | Income-based Job Seekers Allowance                       | No                 |
  | Guarantee State Pension Credit                           | No                 |
  | Income-related Employment and Support Allowance          | No                 |
  | Are you on National Asylum Support Service benefits?     | No                 |
  And The legal help form "Your Property" section has the values
  | field                                                    | main property      | additional property | second property  |
  | Do you own any property?                                 | No                 | N/A                 | N/A              |
  | Property Value                                           | £                  | £                   | £                |
  | Outstanding Mortage                                      | £                  | £                   | £                |
  | Percentage Share                                         | %                  | %                   | %                |
  And The legal help form "Your Capital" section has the values
  | field                                                    | subject matter     | your capital        | partners capital |
  | Savings                                                  | £                  | £0.00               | £                |
  | Investments                                              | £                  | £0.00               | £                |
  | Valuable Items                                           | £                  | £0.00               | £                |
  | Other Capital                                            | £                  | £0.00               | £                |
  | Pensioner Capital Disregard                              | £0.00              | N/A                 | N/A              |
  | TOTAL CAPITAL for Assessment Purposes                    | £0.00              | N/A                 | N/A              |
  And The legal help form "Your Income" section has the values
  | field                                                    | your               | partner             |
  | Wages                                                    | £0.00              | £0.00               |
  | Self Employed Drawings                                   | £0.00              | £0.00               |
  | Benefits                                                 | £0.00              | £0.00               |
  | Tax Credits                                              | £0.00              | £0.00               |
  | Child Benefit                                            | £0.00              | N/A                 |
  | Maintenance Received                                     | £0.00              | £0.00               |
  | Pension Income                                           | £0.00              | £0.00               |
  | Any Other Income                                         | £0.00              | £0.00               |
  | TOTAL INCOME                                             | £0.00              | £0.00               |
  And The legal help form Your Income section (less Monthly allowances) has the values
  | field                                                    | your               | partner             |
  | Tax                                                      | £0.00              | £0.00               |
  | National Insurance                                       | £0.00              | £0.00               |
  | Rent                                                     | £0.00              | £0.00               |
  | Maintenance Payments being made                          | £0.00              | £0.00               |
  | Childcare Costs due to Work                              | £0.00              | £0.00               |
  | Legal Aid payments for Criminal Defence                  | £0.00              | £0.00               |
  | Employment Expenses (standard £45 if employed)           | £                  | £                   |
  | Dependants Allowance (certain amount for each dependant) | £                  | N/A                 |
  | Partner Allowance                                        | £                  | N/A                 |
  | TOTAL MONTHLY DISPOSABLE INCOME                          | £                  | N/A                 |