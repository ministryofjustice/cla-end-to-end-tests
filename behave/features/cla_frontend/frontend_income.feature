@cla_frontend
Feature: - Testing income limits

Background: Login
    Given I am logged in as "CHS_GENERAL_USER"

@income_limit_dropdown
Scenario: Ensure that the dropdowns appear on income
    Given I select to 'Create a case'
    And I have created a user
    And I have created a valid discrimination scope
    And I am on the financial page which i complete up to finances
    And I am on the income tab which i complete with the maximum value
    Then The <dropdown> contains the correct <value>
    | dropdown                                                        | value       |
    | What did you earn before tax? (Check your most recent payslips) | per month   |
    | How much tax do you pay?                                        | per month   |
    | How much National Insurance do you pay?                         | per month   |
    | Self employed drawings (Before Tax)                             | per month   |
    | Benefits                                                        | per month   |
    | Tax credits                                                     | per month   |
    | Child Benefit (for household)                                   | per month   |
    | Maintenance received                                            | per month   |
    | Pension income                                                  | per month   |
    | Other income                                                    | per month   |

@income_limit_dropdown_fail
Scenario: Ensure that the dropdowns appear on income
    Given I select to 'Create a case'
    And I have created a user
    And I have created a valid discrimination scope
    And I am on the financial page which i complete up to finances
    And I am on the income tab which i complete with incorrect values
    Then The <dropdown> contains no values
    | dropdown                                                        |
    | What did you earn before tax? (Check your most recent payslips) |
    | How much tax do you pay?                                        |
    | How much National Insurance do you pay?                         |
    | Self employed drawings (Before Tax)                             |
    | Benefits                                                        |
    | Tax credits                                                     |
    | Child Benefit (for household)                                   |
    | Maintenance received                                            |
    | Pension income                                                  |
    | Other income                                                    |