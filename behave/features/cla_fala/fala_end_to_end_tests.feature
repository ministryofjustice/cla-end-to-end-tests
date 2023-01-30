Feature: FALA end to end tests
  - Testing the search tool
  - Testing to apply filters to the search tool
  - Testing the translation

  Background: Homepage page
    Given I am on the Find a legal aid adviser homepage

  @fala-search-location
  Scenario Outline: Search for legal advisers via postcode and city
    Given I provide the "<location>" details
    When I select the 'search' button on the FALA homepage
    Then I am taken to the page corresponding to "<location>" result
    Examples:
      | location |
      | SW1H9AJ |
      | London   |