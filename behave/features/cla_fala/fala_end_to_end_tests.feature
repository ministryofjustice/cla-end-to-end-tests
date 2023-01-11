Feature: FALA end to end tests
  - Testing the search tool
  - Testing to apply filters to the search tool
  - Testing the translation


  Scenario Outline: Search for legal advisers via postcode and city
    Given I am on the Find a legal aid adviser homepage
    And I provide the "<location>" details via the text input “postcode / city“
    When I click the Search button
    Then I am taken to the search "<results>" page

    Examples: Postcode and city
      | location | results     |
      | SW1H 9AJ | 1 National Council For Civil Liberties      |
      | London   | 1 Boothroyds LLP |
