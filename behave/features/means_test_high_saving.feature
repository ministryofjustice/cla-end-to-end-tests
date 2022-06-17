Feature: Means test failure - high savings
  As a CHS operator, when I manually entered a clients finances to the below results set,
  I get a message that the client is not eligible for Legal Aid

Background: Login and select a case
  Given that I am logged in

@means_test_high_savings
Scenario: Means test display not eligible for Legal Aid message.
  Given I select to 'Create a case'
  And I am on the Finances tab with the ‘Details’ sub-tab preselected
  And I do not have a partner
  And I am not aged 60 or over
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
  Then I move onto Income inner-tab
  And I am not self employed
  And I <answer> to Income <question>
      | question                                                        | answer |
      | What did you earn before tax? (Check your most recent payslips) | 0.00   |
      | How much tax do you pay?                                        | 0.00   |
      | How much National Insurance do you pay?                         | 0.00   |
      | Self employed drawings (Before Tax)                             | 0.00   |
      | Benefits                                                        | 0.00   |
      | Tax credits                                                     | 0.00   |
      | Child Benefit (for household)                                   | 0.00   |
      | Maintenance received                                            | 0.00   |
      | Pension income                                                  | 0.00   |
      | Other income                                                    | 0.00   |
  And I have 0 dependants aged 16 and over
  And I have 0 dependants aged 15 and under
  Then I move onto Expenses inner-tab
  And I <answer> to Expenses <question>
      | question                                                            | answer |
      | How much do you pay for your mortgage?                              | 0.00   |
      | How much do you pay for rent?                                       | 0.00   |
      | How much maintenance have you paid during the last calendar month   | 0.00   |
      | Do you have any childcare costs because of work or study?           | 0.00   |
  And I am currently paying 0.00 towards legal aid for criminal defence
  And I select Save assessment
  Then I am given a message 'The means test has been saved. The current result is eligible for Legal Aid'