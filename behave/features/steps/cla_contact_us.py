from behave import step
from features.constants import (
    ClA_CONTACT_US_USER,
    CLA_CONTACT_US_USER_PERSON_TO_CALL,
    CLA_NUMBER,
)
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import StaleElementReferenceException


@step("I select 'Contact us' from the banner")
def step_impl(context):
    link = context.helperfunc.find_by_xpath("//span/a[text()='Contact us']")
    link.click()


@step("I select <question> from the contact civil legal advice page")
def step_impl(context):
    # Find the question by label
    # Find input and insert value from answer
    for row in context.table:
        label = row["question"]
        checkbox = context.helperfunc.find_by_xpath(
            f"//div/label[contains(text(), '{label}')]"
        )
        checkbox.click()


@step("I click 'continue to contact CLA'")
def step_impl(context):
    context.execute_steps(
        """
        Given I click continue
    """
    )


@step("I select 'Submit details'")
def step_impl(context):
    context.execute_steps(
        """
        Given I click continue
    """
    )


@step("I enter a name in the 'Your full name' field")
def step_impl(context):
    value = ClA_CONTACT_US_USER
    full_name_input = context.helperfunc.find_by_xpath("//input[@id='full_name']")
    full_name_input.send_keys(value)
    assert full_name_input.get_attribute("value") == value


@step("I am on the Contact Civil Legal Advice page")
def step_impl(context):
    context.execute_steps(
        """
        Given I select 'Contact us' from the banner
        And I select <question> from the contact civil legal advice page
            | question                       |
            | I’d prefer to speak to someone |
        And I click 'continue to contact CLA'
        And I am taken to the "Contact Civil Legal Advice" page located on "/contact"
    """
    )


@step("I select the contact option 'Call someone else instead of me'")
def step_impl(context):
    # input can not be found without first finding form
    context.callback_form = context.helperfunc.find_by_xpath("//form")
    callback_element = context.callback_form.find_element_by_xpath(
        '//input[@value="thirdparty"]'
    )
    assert callback_element is not None
    callback_element.click()
    assert callback_element.get_attribute("value") == "thirdparty"


@step("I select 'Call today'")
def step_impl(context):
    # input can not be found without first finding form
    context.callback_form = context.helperfunc.find_by_xpath("//form")
    call_today = context.callback_form.find_element_by_xpath(
        '//input[@value="today"]' '[@id="thirdparty-time-specific_day-0"]'
    )
    assert call_today is not None
    call_today.click()
    assert call_today.get_attribute("value") == "today"


# call someone else instead of me name input field
@step("I enter the full name of the person to call")
def step_impl(context):
    value = CLA_CONTACT_US_USER_PERSON_TO_CALL
    callback_form = context.helperfunc.find_by_xpath("//form")
    full_name_input = callback_form.find_element_by_xpath(
        "//input[@id='thirdparty-full_name'][@name='thirdparty-full_name']"
    )
    full_name_input.send_keys(value)
    assert full_name_input.get_attribute("value") == value


# call someone else instead of me phone number input field
@step("I enter the phone number of the person to call back")
def step_impl(context):
    value = CLA_NUMBER
    callback_form = context.helperfunc.find_by_xpath("//form")
    full_name_input = callback_form.find_element_by_xpath(
        "//input[@id='thirdparty-contact_number']"
    )
    full_name_input.send_keys(value)
    assert full_name_input.get_attribute("value") == value


@step("I select \"{option}\" from the 'Relationship to you' drop down options")
def step_impl(context, option):
    context.callback_form = context.helperfunc.find_by_xpath("//form")
    select = Select(
        context.callback_form.find_element_by_xpath(
            '//select[@id="thirdparty-relationship"]'
        )
    )
    assert select is not None
    try:
        select.select_by_visible_text(option)
    except StaleElementReferenceException:
        assert False, f"Could find {option} in 'Relationship to you select' options"
