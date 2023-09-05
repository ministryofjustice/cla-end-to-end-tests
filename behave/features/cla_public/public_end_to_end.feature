@cla_public
Feature:
  - Applying for legal aid on the "Check if I can get legal aid" website

  Background: Start page
    Given I have selected the start now button on the start page
    And I am taken to the "Choose the area you most need help with" page located on "/scope/diagnosis/"

  @exit-behaviour-button
  Scenario: Describes how to exit from the domestic abuse section and the website safely when clicking the exit button
    When I select the category <category>
      | category       |
      | Domestic abuse |
    Then I am taken to the "Choose the option that best describes your personal situation" page located on "/scope/diagnosis/n43n3"
    Then I click on the "Exit this page" button
    And I am diverted to the BBC website

  @exit-behaviour-keypress
  Scenario: Describes how to exit from the domestic abuse section and the website safely when pressing the escape key
    When I select the category <category>'
      | category       |
      | Domestic abuse |
    Then I am taken to the "Choose the option that best describes your personal situation" page located on "/scope/diagnosis/n43n3"
    Then I press the "esc" key on the keyboard
    And I am diverted to the BBC website