from behave import step

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


@step('I click on the "Exit this page" button')
def step_impl_click_exit_page(context):
    context.helperfunc.click_button(By.CLASS_NAME, "govuk-exit-this-page")


@step('I press the "{keypress}" key "{amount_of_time}" on the keyboard')
def step_impl_keypress_multiple_times(context, keypress, amount_of_time):
    context.helperfunc.find_by_class("govuk-js-exit-this-page-skiplink")

    if (
        len(amount_of_time) == 3
        and ActionChains(webdriver).send_keys(Keys.SHIFT).perform()
    ):
        step_impl_diversion_link()
    if (
        len(amount_of_time) == 2
        and ActionChains(webdriver).send_keys(Keys.TAB).perform()
    ):
        step_impl_diversion_link()


@step('I am diverted to the BBC website "{website}"')
def step_impl_diversion_link(context, website):
    href_bbc_address = context.helperfunc.find_by_xpath(
        "/html/body/div/div/div/a"
    ).get_attribute("href")
    assert href_bbc_address == website

    return context.helperfunc.get_current_path() == website
