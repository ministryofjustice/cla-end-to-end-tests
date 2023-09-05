from behave import step

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


@step('I click on the "Exit this page" button')
def step_impl_click_exit_page(context):
    context.helperfunc.click_button(By.CLASS_NAME, ".govuk-exit-this-page")


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
