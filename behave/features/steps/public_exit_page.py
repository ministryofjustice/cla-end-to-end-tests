from behave import step

from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from helper.constants import BBC_WEBSITE


@step('The "Exit this page" button is on the page and I click it')
def step_impl_click_exit_page(context):
    href_bbc_address = context.helperfunc.find_by_xpath(
        "//main/div/div/a[contains(text(), 'Exit this page')]"
    ).get_attribute("href")

    assert href_bbc_address == BBC_WEBSITE

    context.helperfunc.click_button(By.CLASS_NAME, "govuk-exit-this-page")


@step('I press the "{keypress}" key {amount_of_time} times on the keyboard')
def step_impl_keypress_multiple_times(context, keypress, amount_of_time):
    key_to_press = (
        Keys.SHIFT if keypress == "shift" else Keys.TAB if keypress == "tab" else None
    )

    for _ in range(int(amount_of_time)):
        if key_to_press:
            ActionChains(context.helperfunc.driver()).send_keys(key_to_press).perform()

    if keypress == "tab":
        ActionChains(context.helperfunc.driver()).send_keys(Keys.ENTER).perform()


@step("I am diverted to the BBC website")
def step_impl_diversion_link(context):
    assert context.helperfunc.get_url() == BBC_WEBSITE
