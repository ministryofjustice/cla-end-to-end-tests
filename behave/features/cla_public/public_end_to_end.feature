@cla_public
Feature:
  - Applying for legal aid on the "Check if I can get legal aid" website

Background: Start page
    Given I am applying for legal aid on the "Check if I can get legal aid" website
    And I have selected the start now button on the start page
    And I should be on the diagnosis page "Choose the area you most need help with"

@exit-behaviour-button, @a11y-check
Scenario: Describes how to exit from the domestic abuse section and the website safely when clicking a button
  Given I select the "Domestic abuse" section
  And I should be on the "Choose the option that best describes your personal situation" page
  Then I click on the "Exit this page" button
  And I am diverted to the BBC website

@exit-behaviour-keypress, @a11y-check
Scenario: Describes how to exit from the domestic abuse section and the website safely when pressing a key
  Given I select the "Domestic abuse" section
  And I should be on the "Choose the option that best describes your personal situation" page
  Then I press the "esc" key on the keyboard
  And I am diverted to the BBC website