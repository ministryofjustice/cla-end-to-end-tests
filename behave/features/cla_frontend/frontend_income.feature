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
    And I select Save assessment
    And I refresh the page
    Then I assert that the <question> still have the correct <value> and <dropdown>
    | question                                                        | value         | dropdown    |
    | What did you earn before tax? (Check your most recent payslips) | 99999999.99   | per month   |
    | How much tax do you pay?                                        | 99999999.99   | per month   |
    | How much National Insurance do you pay?                         | 99999999.99   | per month   |
    | Self employed drawings (Before Tax)                             | 99999999.99   | per month   |
    | Benefits                                                        | 99999999.99   | per month   |
    | Tax credits                                                     | 99999999.99   | per month   |
    | Child Benefit (for household)                                   | 99999999.99   | per month   |
    | Maintenance received                                            | 99999999.99   | per month   |
    | Pension income                                                  | 99999999.99   | per month   |
    | Other income                                                    | 99999999.99   | per month   |

@property_disputed_error
Scenario: Ensure that the property disputed error appears
    Given I select to 'Create a case'
    And I have created a user
    And I have created a valid debt case
    And I move onto Finances inner-tab
    And I click 'Add Property'
    Then The error "Please select whether the property is disputed" is returned