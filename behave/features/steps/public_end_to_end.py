from behave import step
from selenium.webdriver.common.by import By


@step('I select the "{section_name}" section')
def step_impl_select_section_name(context, section_name):
    context.helperfunc.click_button(By.LINK_TEXT, section_name)


@step('I should be on the "{diagnosis_title}" page')
def step_impl_diagnosis_title(context, diagnosis_title):
    diagnosis_title_xpath = context.helperfunc.By.CLASS_NAME(".govuk-exit-this-page")
    assert diagnosis_title_xpath == diagnosis_title


@step('I click on the "Exit this page" button')
def step_impl_click_exit_page(context):
    context.helperfunc.find_by_xpath(
        '//html/body/div[3][@class="govuk-exit-this-page"]'
    )
