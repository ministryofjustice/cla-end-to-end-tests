from behave import step

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


@step('I click on the "Exit this page" button')
def step_impl_click_exit_page(context):
    context.helperfunc.click_button(By.CLASS_NAME, "govuk-exit-this-page")


@step('I press the "esc" key on the keyboard')
def step_impl_press_esc_key(context):
    context.helperfunc.find_element_by_class_name("govuk-exit-this-page")
    ActionChains(webdriver).send_keys(Keys.ESCAPE).perform()


@step('I am diverted to the BBC website "{website}"')
def step_impl_diversion_link(context, website):
    href_link = context.helperfunc.find_by_xpath(
        "/html/body/div/div/div/a"
    ).get_attribute("href")

    assert href_link == f"{website}"
