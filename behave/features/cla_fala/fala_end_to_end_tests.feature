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
      | SW1H9AJ  |
      | London   |


  @fala-apply-filter-after-search
  Scenario Outline: Applying filters on the result page provide a new result list of legal advisers
    Given I provide the "<location>" details
    When I select the 'search' button on the FALA homepage
    Then I am taken to the page corresponding to "<location>" result
    When I browse through the filter categories and select "<filter_label>"
    And I select the 'Apply filter' button
    Then the result page containing "<location>" is updated to apply the filter "<filter_label>"
    Examples:
      | location | filter_label |
      | SW1H9AJ  | crm          |
      | London   | hou          |


  @fala-search-no-results
  Scenario: I search for a town that does not have any solicitors and fails
  Given I am on the Find a legal aid adviser homepage
  And I provide the "Heswall" details
  When I select the 'search' button on the FALA homepage
  Then the page shows an error

  @fala-search-organisation
  Scenario Outline: Search by organisation name
    Given I provide the "<location>" details
    And I provide an organisation name "<organisation>"
    When I select the 'search' button on the FALA homepage
    Then I am taken to the page corresponding to the "<location>" "<organisation>" search result
    And 1 result is visible on the results page
    Examples:
          | location |  organisation  |
          | London   | Boothroyds LLP |


  @dom-translation
  Scenario Outline: Selecting a language correctly updates the DOM
    When I select the language "<language>" and select "<code_indicator>"
    And the page is updated to "<code_indicator>" and title starts with "<title_text_starts_with>"
    Examples:
      | code_indicator | language     | title_text_starts_with |
      | cy             | Welsh        | Dewch                  |
     # | ee             | Ewe          |
     # | ga             | Irish Gaelic |
     # | gd             | Scots Gaelic |
