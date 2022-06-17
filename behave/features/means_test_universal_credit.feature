Feature: Means test assessment - universal credit
    Confirming that when a person:

    - Does not have a partner
    - Is aged 60 or over
    - Is on universal credit benefits
    - Has no savings in the bank
    - Has no investments, shares or ISAs
    - Has no valuable items worth over £500 each
    - Has no money owed to them

    That they are eligble for legal aid and can be assigned a provider

Background: Login
    Given that I am logged in

@means_test_universal
Scenario: Successful means test assessment resulting in user being eligible for legal aid
    Given I select to 'Create a case'
    And I am on the Finances tab with the ‘Details’ sub-tab preselected
    When I do not have a partner
    And I am not aged 60 or over
    And I <answer> to Details <question>
        | question                                                        | answer |
        | Universal credit                                                | Yes    |
    And I move onto Finances inner-tab
    And I <answer> to Finances <question>
        | question                                               | answer |
        | How much was in your bank account/building             | 0.00   |
        | Do you have any investments, shares or ISAs?           | 0.00   |
        | Do you have any valuable items worth over £500 each?   | 0.00   |
        | Do you have any money owed to you?                     | 0.00   |
    And I select Save assessment
    Then I am given a message 'The means test has been saved. The current result is eligible for Legal Aid'
    And the 'Diversity' and 'Assign' tabs become available
