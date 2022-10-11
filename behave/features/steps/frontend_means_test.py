from behave import step
import re
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from helper.constants import CLA_FRONTEND_PERSONAL_DETAILS_FORM


def set_income_input_field_by_label(context, label, value):
    # income input fields under case details page as more HTML elements
    # to navigate through.
    context.helperfunc.find_by_xpath(f"//span[text()='{label}']/../../input").send_keys(
        value
    )


def set_income_input_field_by_label_for(context, label, value):
    # At the bottom of case details page under the income inner tab
    # Can not get element via text as it's broken up.
    # No idea to target but id string is being used in label for attribute.
    context.helperfunc.find_by_xpath(f"//label[@for='{label}']/input").send_keys(value)


@step("I am on the Finances tab with the ‘Details’ sub-tab preselected")
def step_impl_finance_details_tabs(context):
    context.execute_steps(
        """
        Given I have created a valid discrimination scope
        Then I am taken to the Finances tab with the ‘Details’ sub-tab preselected
    """
    )


@step("I move onto {tab_name} inner-tab")
def step_impl_move_to_tab(context, tab_name):
    xpath_scroll = "//form/div[contains(@class,'Toolbar')]"
    page = context.helperfunc
    actions = ActionChains(page.driver())
    actions.move_to_element(page.find_by_xpath(xpath_scroll)).perform()

    xpath = f"//ul[@id='pills-section-list']/li/a[text()='{tab_name}']"
    WebDriverWait(page.driver(), 10).until(
        EC.element_to_be_clickable((By.XPATH, xpath))
    ).click()

    def wait_for_active_tab(*args):
        return tab_name in context.helperfunc.find_by_class("Pills-pill.is-active").text

    wait = WebDriverWait(context.helperfunc.driver(), 10)
    wait.until(wait_for_active_tab)


@step("I select Save assessment")
def step_impl_save_assessment(context):
    button = context.helperfunc.find_by_name("save-means-test")
    button.click()


@step("the 'Diversity' and 'Assign' tabs become available")
def step_impl_diversity_and_assign_available(context):
    page = context.helperfunc
    diversity_tab = page.find_by_partial_link_text("Diversity")
    assert "is-disabled" not in diversity_tab.get_attribute("class")
    assign_tab = page.find_by_partial_link_text("Assign")
    assert "is-disabled" not in assign_tab.get_attribute("class")


@step("I <answer> to Income <question>")
def step_impl_answer_income_question(context):
    # Find the question by label
    # Find input and insert value from answer
    for row in context.table:
        label = row["question"]
        value = row["answer"]
        set_income_input_field_by_label(context, label, value)


@step("I <answer> to Details <question>")
def step_impl_answer_details_question(context):
    # Find the question by label
    # Find input and insert value from answer
    for row in context.table:
        label = row["question"]
        value = row["answer"]
        if value == "No":
            question_radio_value = "false"
        elif value == "Yes":
            question_radio_value = "true"
        else:
            raise ValueError(f"Can only process Yes or No answers. You entered {value}")
        context.helperfunc.find_by_xpath(
            f"//p[text()='{label}']/../label/input[@value='{question_radio_value}']"
        ).click()


@step("I <answer> to Finances <question>")
def step_impl_answer_finance_question(context):
    # Find the question by label
    # Find input and insert value from answer
    for row in context.table:
        label = row["question"]
        value = row["answer"]
        label_format = label.ljust(len(label) + 1)
        # Each question under the finances inner tab
        # has a space character at the end of string
        # Using ljust method to add space character
        context.helperfunc.find_by_xpath(
            f"//span[contains(text(),'{label_format}')]/../input"
        ).send_keys(value)


@step("I <answer> to Expenses <question>")
def step_impl_answer_expense_question(context):
    # Find the question by label
    # Find input and insert value from answer
    for row in context.table:
        label = row["question"]
        value = row["answer"]
        context.helperfunc.find_by_xpath(
            f"//label/span/span[contains(text(), '{label}')]/../../input"
        ).send_keys(value)


@step("I have {number:d} dependants aged 16 and over")
def step_impl_number_of_dependants_over(context, number):
    set_income_input_field_by_label_for(context, "id_dependants-dependants_old", number)


@step("I have {number:d} dependants aged 15 and under")
def step_impl_number_of_dependants_under(context, number):
    set_income_input_field_by_label_for(
        context, "id_dependants-dependants_young", number
    )


@step("I am currently paying {numbers:f} towards legal aid for criminal defence")
def step_impl_paying_defence(context, numbers):
    # In order to use float in send keys method.
    # float needs to be converted to a string.
    numbers_to_string = str(numbers)
    input_field = context.helperfunc.find_by_xpath(
        "//label/span[@class='FormRow-label ng-binding']/../input[@type='number']"
    )
    input_field.send_keys(numbers_to_string)


@step("I am taken to the 'case details' page")
def step_impl_case_details(context):
    assert context.helperfunc.find_by_xpath("//header/h1").text == "Case details"
    current_path = context.helperfunc.get_current_path()
    assert re.match(r"^/call_centre/\w{2}-\d{4}-\d{4}/diagnosis/$", current_path)


@step("I select 'Create new user'")
def step_impl_create_user(context):
    btn = context.helperfunc.find_by_name("create-newuser")
    assert btn is not None
    btn.click()
    form = context.helperfunc.find_by_name("personaldetails_frm")
    assert form.is_displayed()


@step("enter the client's personal details")
def step_impl_enter_details(context):
    if not hasattr(context, "personal_details_form"):
        context.personal_details_form = CLA_FRONTEND_PERSONAL_DETAILS_FORM
    for name, value in context.personal_details_form.items():
        element = context.helperfunc.find_by_name(name)
        assert element is not None
        if element.tag_name == "select":
            select_element = Select(element)
            select_element.select_by_visible_text(value)
        else:
            element.send_keys(value)


@step("I click the save button on the screen")
def step_impl_click_save_button(context):
    form = context.helperfunc.find_by_name("personaldetails_frm")
    btn = context.helperfunc.find_by_name("save-personal-details")
    assert btn is not None
    btn.click()

    def wait_until_personal_details_are_saved(*args):
        return not form.is_displayed()

    wait = WebDriverWait(context.helperfunc.driver(), 10)
    wait.until(wait_until_personal_details_are_saved)


@step("I will see the users details")
def step_impl_user_details(context):
    personal_details = context.helperfunc.find_by_id("personal_details").text
    for name, value in context.personal_details_form.items():
        assert value in personal_details
