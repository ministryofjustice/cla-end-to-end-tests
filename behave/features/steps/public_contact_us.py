from behave import step
from helper.constants import (
    ClA_CONTACT_US_USER,
    CLA_CONTACT_US_USER_PERSON_TO_CALL,
    CLA_NUMBER,
    CONTACT_US_OPTIONS,
)
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import (
    StaleElementReferenceException,
    NoSuchElementException,
)


@step("I select 'Contact us' from the banner")
def step_impl_select_contact_us(context):
    link = context.helperfunc.find_by_xpath("//span/a[text()='Contact us']")
    link.click()


@step("I select <question> from the contact civil legal advice page")
def step_impl_select_question_on_cla_page(context):
    # Find the question by label
    # Find input and insert value from answer
    for row in context.table:
        label = row["question"]
        checkbox = context.helperfunc.find_by_xpath(
            f"//div/label[contains(text(), '{label}')]"
        )
        checkbox.click()


@step("I click 'continue to contact CLA'")
def step_impl_click_contact_cla(context):
    context.execute_steps(
        """
        Given I click continue
    """
    )


@step("I select 'Submit details'")
def step_impl_submit_details(context):
    context.execute_steps(
        """
        Given I click continue
    """
    )


@step("I enter a name in the 'Your full name' field")
def step_impl_enter_a_full_name(context):
    value = ClA_CONTACT_US_USER
    full_name_input = context.helperfunc.find_by_xpath("//input[@id='full_name']")
    full_name_input.send_keys(value)
    assert full_name_input.get_attribute("value") == value


@step("I am on the Contact Civil Legal Advice page")
def step_impl_contact_cla_page(context):
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


@step("I select the contact option '{option}'")
def step_impl_select_call_someone_else(context, option):
    radio_option = ""

    for key, value in CONTACT_US_OPTIONS.items():
        if key in option:
            radio_option = value
            break

    # input can not be found without first finding form
    context.callback_form = context.helperfunc.find_by_xpath("//form")
    callback_element = context.callback_form.find_element_by_xpath(
        f'//input[@value="{radio_option}"]'
    )
    assert callback_element is not None
    callback_element.click()
    assert callback_element.get_attribute("value") == f"{radio_option}"


@step('I select the next available "{option}" time slot')
def step_impl_select_next_available_time_slot(context, option):
    def is_call_today_option_visible(*args):
        try:
            context.callback_form.find_element_by_xpath(
                '//input[@value="today"]' '[@id="thirdparty-time-specific_day-0"]'
            )
            return True
        except NoSuchElementException:
            return False

    context.callback_form = context.helperfunc.find_by_xpath("//form")
    if is_call_today_option_visible() is True:
        call_today = context.callback_form.find_element_by_xpath(
            '//input[@value="today"]' '[@id="thirdparty-time-specific_day-0"]'
        )
        call_today.click()
        assert call_today.get_attribute("value") == "today"
        assert_select_first_dropdown(
            context, f'//select[@id="{option}-time-time_today"]'
        )
    else:
        specific_day = context.callback_form.find_element_by_xpath(
            '//input[@value="specific_day"]' '[@id="thirdparty-time-specific_day-1"]'
        )
        specific_day.click()
        assert specific_day.get_attribute("value") == "specific_day"
        assert_select_first_dropdown(context, f'//select[@id="{option}-time-day"]')
        assert_select_first_dropdown(
            context, f'//select[@id="{option}-time-time_in_day"]'
        )


def assert_select_first_dropdown(context, xpath_id):
    choose_first_item = Select(context.callback_form.find_element_by_xpath(xpath_id))
    assert choose_first_item is not None
    if len(choose_first_item.options) > 0:
        choose_first_item.select_by_index(1)
    else:
        raise AssertionError(f"No option in dropdown menu {xpath_id}")


# call someone else instead of me name input field
@step("I enter the full name of the person to call")
def step_impl_enter_name(context):
    value = CLA_CONTACT_US_USER_PERSON_TO_CALL
    callback_form = context.helperfunc.find_by_xpath("//form")
    full_name_input = callback_form.find_element_by_xpath(
        "//input[@id='thirdparty-full_name'][@name='thirdparty-full_name']"
    )
    full_name_input.send_keys(value)
    assert full_name_input.get_attribute("value") == value


# call me back input field
@step("I enter my full name")
def step_impl_my_full_enter_name(context):
    value = CLA_CONTACT_US_USER_PERSON_TO_CALL
    callback_form = context.helperfunc.find_by_xpath("//form")
    full_name_input = callback_form.find_element_by_xpath(
        "//input[@id='callback-full_name'][@name='callback-full_name']"
    )
    full_name_input.send_keys(value)
    assert full_name_input.get_attribute("value") == value


# call someone else instead of me phone number input field
@step("I enter the phone number of the person to call back")
def step_impl_enter_phone_number(context):
    value = CLA_NUMBER
    callback_form = context.helperfunc.find_by_xpath("//form")
    full_name_input = callback_form.find_element_by_xpath(
        "//input[@id='thirdparty-contact_number']"
    )
    full_name_input.send_keys(value)
    assert full_name_input.get_attribute("value") == value


# the users phone number
@step("I enter my phone number")
def step_impl_enter_my_phone_number(context):
    value = CLA_NUMBER
    callback_form = context.helperfunc.find_by_xpath("//form")
    full_name_input = callback_form.find_element_by_xpath(
        "//input[@id='callback-contact_number']"
    )
    full_name_input.send_keys(value)
    assert full_name_input.get_attribute("value") == value


@step("I select \"{option}\" from the 'Relationship to you' drop down options")
def step_impl_select_relationship_option(context, option):
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


@step("I select '{option}' to announce call options")
def step_impl_select_announce_call_option(context, option):
    value_option = "true" if option == "Yes" else "false"
    context.callback_form = context.helperfunc.find_by_xpath("//form")
    announce_call_radio = context.callback_form.find_element_by_xpath(
        f'//input[@value="{value_option}"]' '[@id="callback-announce_call_from_cla-0"]'
    )
    announce_call_radio.click()
    assert announce_call_radio.get_attribute("value") == f"{value_option}"
