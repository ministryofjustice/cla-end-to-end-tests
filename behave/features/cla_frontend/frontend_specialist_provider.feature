@cla_frontend
Feature: Specialist Provider Case Assignment
# Testing fixture used is loaded as part of creat_db.sh file.

Background: Log In Provider
    Given I am logged in as "TEST_SPECIALIST_PROVIDER"

@specialist-provider-select-case
Scenario: Specialist Provider Selects a case
  Given I am on the specialist provider cases dashboard page
  And there is a case available
  And I select a "CLA_SPECIALIST_CASE_TO_ACCEPT" case from the dashboard
  And I am taken to the "specialist provider" case details page
  And I can view the client details
  | details     |
  | Full name   |
  And I can view the case details and notes entered by the Operator
  When I select Scope
  Then I can view the scope assessment entered by the Operator
  When I select Finances
  Then I can view the financial assessment entered by the Operator

@specialist-provider-accept-case
Scenario: Specialist Provider Accepts a case
  Given I am on the specialist provider cases dashboard page
  And there is a case available
  And I select a "CLA_SPECIALIST_CASE_TO_ACCEPT" case from the dashboard
  And I am taken to the "specialist provider" case details page
  And I select 'Accept' in the case details page
  And I can see a 'Case accepted successfully' message
  When I return to the specialist provider cases dashboard page
  And I select the Accepted tab
  Then I can see my accepted case reference number

@specialist-provider-select-legal-help-form
Scenario: Specialist Provider Accepts a case and Selects Legal Help Form
  Given I am viewing a case that I have accepted as a specialist provider
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
  | field                                                    | subject matter     | your capital          | partners capital |
  | Savings                                                  | £                  | £0.00                 | £                |
  | Investments                                              | £                  | £0.00                 | £                |
  | Valuable Items                                           | £                  | £0.00                 | £                |
  | Other Capital                                            | £                  | £0.00                 | £                |
  | Pensioner Capital Disregard                              | £0.00              | N/A                   | N/A              |
  | TOTAL CAPITAL for Assessment Purposes                    | £0.00              | N/A                   | N/A              |
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

# p12 reject a case (LGA-1854, LGA-1855)
@specialist-provider-reject-case
Scenario: Specialist Provider rejects a case
  Given I am on the specialist provider cases dashboard page
  And I select a "CLA_SPECIALIST_CASE_TO_REJECT" case from the dashboard
  And I am taken to the "specialist provider" case details page
  And I select 'Reject' in the case details page
  Then the reject modal appears on screen
  And I select a reject reason of 'MIS-OOS'
  And I enter a reason into the Notes textarea
  When I select the 'Reject case' button in the pop-up
  Then I am on the specialist provider cases dashboard page
  And I confirm that my case has an Outcome code of 'MIS-OOS'

# p13 split a case (LGA-1857, LGA-1858)
@specialist-provider-split-case
Scenario: Specialist Provider rejects a case
  Given I am on the specialist provider cases dashboard page
  And I select a "CLA_SPECIALIST_CASE_TO_SPLIT" case from the dashboard
  And I am taken to the "specialist provider" case details page
  And I select 'Split' in the case details page
  Then the split case modal appears on screen
  And the 'New case' drop down values are
  | label           | value                                                                    |
  | Category of law | Education                                                                |
  | Matter type 1   | ESEN - Special educational needs and/or children unable to attend school |
  | Matter type 2   | EDSC - School                                                            |
  And I enter a comment into the new case notes textarea
  And I select 'To operator for assignment' for the 'Assign' radio options
  When I select the 'Split case' button in the pop-up
  Then the message 'Case split successfully' appears on the case details page
  And I select the 'Sign out' link
  And I am logged in as "CHS_GENERAL_USER"
  Then the new split case is available to the operator

# p14 Child 1 & Child 2, Upload a CSV file with errors, then upload a csv with no errors. (LGA-1868, LGA-1871)
@specialist-provider-upload-csv-errors
Scenario: Specialist Provider upload a csv
  Given I am on the CSV upload page
  When I select 'Choose file' and upload an invalid csv file
  Then I select the month and year for the uploaded csv file
  And I select the 'Upload' button
  And I am given details of the errors in each line of the csv file
  # Upload a valid csv file again straight after an error upload
  When I select 'Choose file' and upload an valid csv file
  Then I select the month and year for the uploaded csv file
  And I select the 'Upload' button
  And I check that there are no errors in the csv upload page
  Then I can see the file listed in the uploaded files table

@specialist-provider-edit-case
Scenario: Specialist Provider Edits a case
  Given I am on the specialist provider cases dashboard page
  And I select a "CLA_SPECIALIST_CASE_TO_EDIT" case from the dashboard
  And I am taken to the "specialist provider" case details page
  And I select Finances
  And I move onto Finances inner-tab
  And I <answer> to Finances <question>
    | question                                                                                      | answer |
    | How much was in your bank account/building society before your last payment went in?          | 500    |
    | Do you have any investments, shares or ISAs?                                                  | 0      |
    | Do you have any valuable items worth over £500 each?                                          | 0      |
    | Do you have any money owed to you?                                                            | 0      |
  When I select Save assessment
  And I am given a message 'The means test has been saved. The current result is eligible for Legal Aid'
  And I return to the specialist provider cases dashboard page
  And I search for and select a "CLA_SPECIALIST_CASE_TO_EDIT" case
  And I select Finances
  And I move onto Finances inner-tab
  Then I can see on Finances inner-tab <question> that the <answer> remain updated
    | question                                                                                      | answer |
    | How much was in your bank account/building society before your last payment went in?          | 500    |
    | Do you have any investments, shares or ISAs?                                                  | 0      |
    | Do you have any valuable items worth over £500 each?                                          | 0      |
    | Do you have any money owed to you?                                                            | 0      |


@legal_help_form_above_18_no_follow_up_questions
Scenario: No to under 17 question appears in the Legal Help Form
  Given I am on the specialist provider cases dashboard page
  And I select a "CLA_SPECIALIST_CASE_TO_EDIT" case from the dashboard
  Then I am taken to the "specialist provider" case details page
  And I select the "Finances" tab on the specialist provider case page
  And I am not aged 17 or under
  And I select Save assessment
  When I accept the case and open the Legal Help Form
  And I am taken to the cases Legal Help Form
  Then <question> is visible with value <answer> in the form
  | question                                  | answer |
  | Are you aged 17 or under?                 | No     |
  | Do you have a partner that you live with? | No     |


@legal_help_form_under_18_receives_money_regularly
Scenario: Yes for under 18 and regular payments does not receive follow up question
  Given I am on the specialist provider cases dashboard page
  And I select a "CLA_SPECIALIST_CASE_TO_EDIT" case from the dashboard
  Then I am taken to the "specialist provider" case details page
  And I select the "Finances" tab on the specialist provider case page
  When I am aged 17 or under
  And I do receive money on a regular basis
  And I select Save assessment
  When I accept the case and open the Legal Help Form
  And I am taken to the cases Legal Help Form
  Then <question> is visible with value <answer> in the form
    | question                                      | answer |
    | Are you aged 17 or under?                     | Yes    |
    | Do you receive any money on a regular basis?  | Yes    |
    | Do you have a partner that you live with?     | No     |


@legal_help_form_under_18_has_valuables
Scenario: Yes to under 18 with valuables over 2500 proceeds to fill means testing
  Given I am on the specialist provider cases dashboard page
  And I select a "CLA_SPECIALIST_CASE_TO_EDIT" case from the dashboard
  Then I am taken to the "specialist provider" case details page
  And I select the "Finances" tab on the specialist provider case page
  When I am aged 17 or under
  And I do not receive money on a regular basis
  And I do have savings, items of value or investments totalling £2500 or more
  And I select Save assessment
  When I accept the case and open the Legal Help Form
  And I am taken to the cases Legal Help Form
  Then <question> is visible with value <answer> in the form
    | question                                                                         | answer |
    | Are you aged 17 or under?                                                        | Yes    |
    | Do you receive any money on a regular basis?                                     | No     |
    | Do you have any savings, items of value or investments totalling £2500 or more?  | Yes    |
    | Do you have a partner that you live with?                                        | No     |


@legal_help_form_under_18_passported
Scenario: Person aged under 18 is passported is visible on legal help form
  Given I am on the specialist provider cases dashboard page
  And I select a "CLA_SPECIALIST_CASE_TO_EDIT" case from the dashboard
  Then I am taken to the "specialist provider" case details page
  And I select the "Finances" tab on the specialist provider case page
  When I am aged 17 or under
  And I do not receive money on a regular basis
  And I do not have savings, items of value or investments totalling £2500 or more
  And I select Save assessment
  When I accept the case and open the Legal Help Form
  And I am taken to the cases Legal Help Form
  And <question> is visible with value <answer> in the form
    | question                                                                         | answer |
    | Are you aged 17 or under?                                                        | Yes    |
    | Do you receive any money on a regular basis?                                     | No     |
    | Do you have any savings, items of value or investments totalling £2500 or more?  | No     |
  Then <question> is not visible in the form
    | question                                  |
    | Do you have a partner that you live with? |
