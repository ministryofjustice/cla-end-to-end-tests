from behave import *
from selenium.webdriver.common.action_chains import ActionChains
from features.constants import CLA_CASE_DETAILS_INNER_TAB


def set_radio_by_label(context, label, value):
    if value == 'No':
        question_radio_value = "false"
    elif value == 'Yes':
        question_radio_value = "true"
    else:
        raise ValueError(f"Can only process Yes or No answers. You entered {value}")
    context.helperfunc.find_by_xpath(f"//p[text()='{label}']/../label/input[@value='{question_radio_value}']").click()


def set_income_input_field_by_label(context, label, value):
    # income input fields under case details page as more HTML elements
    # to navigate through.
    context.helperfunc.find_by_xpath(f"//span[text()='{label}']/../../input").send_keys(value)


def set_income_input_field_by_label_for(context, label, value):
    # At the bottom of case details page under the income inner tab
    # Can not get element via text as it's broken up.
    # No idea to target but id string is being used in label for attribute.
    context.helperfunc.find_by_xpath(f"//label[@for='{label}']/input").send_keys(value)


def set_expenses_input_field_by_label(context, label, value):
    context.helperfunc.find_by_xpath(f"//label/span/span[contains(text(), '{label}')]/../../input").send_keys(value)


def set_input_field_by_label(context, label, value):
    context.helperfunc.find_by_xpath(f"//span[contains(text(),'{label}')]/../input").send_keys(value)


@step(u'I am on the Finances tab with the ‘Details’ sub-tab preselected')
def step_impl(context):
    context.execute_steps(u'''
        Given I have created a valid discrimination scope
        Then I am taken to the Finances tab with the ‘Details’ sub-tab preselected
    ''')


@step(u'I move onto {tab_name} inner-tab')
def step_impl(context, tab_name):
    # JSON contains list of inner tab names and indexes
    tab_json = CLA_CASE_DETAILS_INNER_TAB
    for key in tab_json:
        index_number = tab_json[key]
        if tab_name == key:
            page = context.helperfunc
            inner_tab = page.find_by_xpath(f"//*[@id='pills-section-list']/li[{index_number}]")
            assert tab_name in inner_tab.text
            actions = ActionChains(page.driver())
            actions.move_to_element(inner_tab).perform()
            inner_tab.click()
            # Confirm inner tab is active
            active_inner_tab = context.helperfunc.find_by_class("Pills-pill.is-active")
            assert tab_name in active_inner_tab.text


@step(u'I select Save assessment')
def step_impl(context):
    button = context.helperfunc.find_by_name("save-means-test")
    button.click()


@step(u'I am given a message \'The means test has been saved. The current result is eligible for Legal Aid\'')
def step_impl(context):
    element = context.helperfunc.find_by_css_selector(".Notice.Notice--closeable.success")
    assert element.text == 'The means test has been saved. The current result is eligible for Legal Aid'


@step(u'the \'Diversity\' and \'Assign\' tabs become available')
def step_impl(context):
    page = context.helperfunc
    diversity_tab = page.find_by_partial_link_text("Diversity")
    assert 'is-disabled' not in diversity_tab.get_attribute("class")
    assign_tab = page.find_by_partial_link_text("Assign")
    assert 'is-disabled' not in assign_tab.get_attribute("class")


@step(u'I <answer> to Income <question>')
def step_impl_means_test(context):
    # Find the question by label
    # Find input and insert value from answer
    for row in context.table:
        label = row['question']
        value = row['answer']
        set_income_input_field_by_label(context, label, value)


@step(u'I <answer> to Details <question>')
def step_impl_means_test(context):
    # Find the question by label
    # Find input and insert value from answer
    for row in context.table:
        label = row['question']
        value = row['answer']
        set_radio_by_label(context, label, value)


@step(u'I <answer> to Finances <question>')
def step_impl_means_test(context):
    # Find the question by label
    # Find input and insert value from answer
    for row in context.table:
        label = row['question']
        value = row['answer']
        label_format = label.ljust(len(label)+1)
        # Each question under the finances inner tab
        # has a space character at the end of string
        # Using ljust method to add space character
        set_input_field_by_label(context, label_format, value)


@step(u'I <answer> to Expenses <question>')
def step_impl_means_test(context):
    # Find the question by label
    # Find input and insert value from answer
    for row in context.table:
        label = row['question']
        value = row['answer']
        set_expenses_input_field_by_label(context, label, value)


@step(u'I have {number:d} dependants aged 16 and over')
def step_impl(context, number):
    set_income_input_field_by_label_for(context, 'id_dependants-dependants_old', number)


@step(u'I have {number:d} dependants aged 15 and under')
def step_impl(context, number):
    set_income_input_field_by_label_for(context, 'id_dependants-dependants_young', number)


@step(u'I am currently paying {numbers:f} towards legal aid for criminal defence')
def step_impl(context, numbers):
    # In order to use float in send keys method.
    # float needs to be converted to a string.
    numbers_to_string = str(numbers)
    input_field = context.helperfunc.find_by_xpath(f"//label/span[@class='FormRow-label ng-binding']/../input[@type='number']")
    input_field.send_keys(numbers_to_string)