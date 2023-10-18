from behave import step
from selenium.webdriver.support.select import Select


@step("I am on the financial page which i complete up to finances")
def step_impl_finance_complete(context):
    context.execute_steps(
        """
        Given I am taken to the "Finances" tab with the ‘Details’ sub-tab preselected
        And I am not aged 17 or under
        And I do not have a partner
        And I am aged 60 or over
        And I <answer> to Details <question>
          | question                                          | answer |
          | Universal credit                                  | No     |
          | Income Support                                    | No     |
          | Income-based Job Seekers Allowance                | No     |
          | Guarantee State Pension Credit                    | No     |
          | Income-related Employment and Support Allowance   | No     |
        Then I move onto Finances inner-tab
        And I <answer> to Finances <question>
          | question                                              | answer |
          | How much was in your bank account/building society    | 0.00   |
          | Do you have any investments, shares or ISAs?          | 0.00   |
          | Do you have any valuable items worth over £500 each?  | 0.00   |
          | Do you have any money owed to you?                    | 0.00   |
        And I select Save assessment
    """
    )


@step("I am on the income tab which i complete with the maximum value")
def step_impl_income_max_complete(context):
    context.execute_steps(
        """
    Then I move onto Income inner-tab
    And I am not self employed
    And I <answer> to Income <question>
    | question                                                        | answer        |
    | What did you earn before tax? (Check your most recent payslips) | 99999999.99   |
    | How much tax do you pay?                                        | 99999999.99   |
    | How much National Insurance do you pay?                         | 99999999.99   |
    | Self employed drawings (Before Tax)                             | 99999999.99   |
    | Benefits                                                        | 99999999.99   |
    | Tax credits                                                     | 99999999.99   |
    | Child Benefit (for household)                                   | 99999999.99   |
    | Maintenance received                                            | 99999999.99   |
    | Pension income                                                  | 99999999.99   |
    | Other income                                                    | 99999999.99   |
    And I have 0 dependants aged 16 and over
    And I have 0 dependants aged 15 and under
    """
    )


@step("The <dropdown> contains the correct <value>")
def step_impl_dropdown_value(context):
    for row in context.table:
        label = row["dropdown"]
        value = row["value"]
        select = Select(
            context.helperfunc.find_by_xpath(f"//span[text()='{label}']/../../select")
        )
        assert select.first_selected_option.text == value


@step("I am on the income tab which i complete with incorrect values")
def step_impl_income_incorrect_value(context):
    context.execute_steps(
        """
    Then I move onto Income inner-tab
    And I am not self employed
    And I <answer> to Income <question>
    | question                                                        | answer  |
    | What did you earn before tax? (Check your most recent payslips) | a       |
    | How much tax do you pay?                                        | a       |
    | How much National Insurance do you pay?                         | a       |
    | Self employed drawings (Before Tax)                             | a       |
    | Benefits                                                        | a       |
    | Tax credits                                                     | a       |
    | Child Benefit (for household)                                   | a       |
    | Maintenance received                                            | a       |
    | Pension income                                                  | a       |
    | Other income                                                    | a       |
    And I have 0 dependants aged 16 and over
    And I have 0 dependants aged 15 and under
    """
    )


@step("The <dropdown> contains no values")
def step_impl_dropdown_no_value(context):
    for row in context.table:
        label = row["dropdown"]
        select = Select(
            context.helperfunc.find_by_xpath(f"//span[text()='{label}']/../../select")
        )
        assert len(select.first_selected_option.text) == 0
