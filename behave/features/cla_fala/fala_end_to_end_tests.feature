Feature: FALA end to end tests
  - Testing the search tool
  - Testing to apply filters to the search tool
  - Testing the translation

  Background: Homepage page
    Given I am on the Find a legal aid adviser homepage

  @fala-search-postcode @a11y-check
  Scenario Outline: Search for legal advisers via postcode
    Given I provide the "<location>" details
    When I select the "search" button on the FALA homepage
    Then I am taken to the page corresponding to "<location>" result
    Examples:
      | location |
      | SW1H 9AJ |


  @fala-search-city @a11y-check
  Scenario Outline: Search for legal advisers via city returns error
    Given I provide the "<location>" details
    When I select the "search" button on the FALA homepage
    Then A "Postcode not found" error is returned
    Examples:
      | location |
      | London |


  @fala-apply-filter-after-search @a11y-check
  Scenario Outline: Applying filters on the result page provide a new result list of legal advisers
    Given I provide the "<location>" details
    When I select the "search" button on the FALA homepage
    Then I am taken to the page corresponding to "<location>" result
    When I browse through the filter categories and select "<filter_label>"
    And I select the "Apply filter" button
    Then the result page containing "<location>" is updated to apply a filter "<filter_label>"
    And there are less results visible on the results page
    Examples:
      | location | filter_label |
      | SW1H 9AJ | crm          |


  @fala-search-organisation @a11y-check
  Scenario Outline: Search by organisation name
    Given I provide the "<location>" details
    And I provide an organisation name "<organisation>"
    When I select the "search" button on the FALA homepage
    Then I am taken to the page corresponding to the "<location>" "<organisation>" search result
    And 1 result is visible on the results page
    Examples:
      | location | organisation   |
      | SW1H 9AJ | Boothroyds LLP |


  @fala-dom-translation @a11y-check
  Scenario Outline: Selecting a language correctly updates the DOM
    When I select the language "<language>" with value "<code_indicator>"
    Then the page is updated to "<code_indicator>" and the title starts with "<title_starts_with>"
    Examples:
      | code_indicator | language     | title_starts_with |
      | cy             | Welsh        | Dewch             |
      | gd             | Scots Gaelic | Lorg              |


  @fala-apply-filter-on-homepage @a11y-check
  Scenario Outline: Applying filters specifically on the homepage, filters correctly
    Given I collect the resulting number for a generic "<location>" search
    When I am on the Find a legal aid adviser homepage
    And I provide the "<location>" details
    And I browse through the filter categories and select "<filter_label>"
    And I select the "Apply filter" button
    Then the result page containing "<location>" is updated to apply a filter "<filter_label>"
    And there are less results visible on the results page
    Examples:
      | location | filter_label |
      | SW1H 9AJ | edu          |
