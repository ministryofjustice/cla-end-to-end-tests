Feature: FALA end to end tests
  - Testing the search tool
  - Testing to apply filters to the search tool
  - Testing the translation

  Background: Homepage page
    Given I am on the Find a legal aid adviser homepage

  @fala-search-location @a11y-check
  Scenario: Search for legal advisers via postcode and city
    Given I provide the "SW1H 9AJ" details
    When I select the "search" button on the FALA homepage
    Then I am taken to the page corresponding to "SW1H 9AJ" result


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
      | PL1 2DP  | hou          |


  @fala-search-no-results @a11y-check
  Scenario: I search for an incorrect postcode that does not have any solicitors and fails
    Given I am on the Find a legal aid adviser homepage
    And I provide the "PL9" details
    When I select the "search" button on the FALA homepage
    Then the page shows an error


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
