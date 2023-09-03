from behave import step

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


@step('I am on the "{homepage_title}" website page')
def step_impl_homepage_title(context, homepage_title):
    homepage_title_xpath = context.helperfunc.find_by_xpath("//main/div[2]/h1")
    assert homepage_title_xpath == homepage_title


@step('I should be on the general diagnosis page "{main_diagnosis_page_title}"')
def step_impl_main_diagnosis_title(context, main_diagnosis_page_title):
    main_diagnosis_page_title_xpath = context.helperfunc.find_by_xpath(
        "//main/div[2]/fieldset/legend/h1"
    )
    assert main_diagnosis_page_title_xpath == main_diagnosis_page_title


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


@step('I press the "esc" key on the keyboard')
def step_impl_press_esc_key(context):
    context.helperfunc.find_element_by_class_name(".govuk-exit-this-page")
    ActionChains(webdriver).send_keys(Keys.ESCAPE).perform()


@step("I am diverted to the BBC website")
def step_impl_diversion_link(context, link_text):
    assert (
        context.helperfunc.find_by_link_text(link_text) is not None
    ), f"Could not find link: {link_text}"

    link_href = context.helperfunc.find_by_link_text(link_text).get_attribute("href")
    context.helperfunc.click_button(By.LINK_TEXT, link_text)

    return link_href
