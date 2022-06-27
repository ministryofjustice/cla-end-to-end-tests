from behave import *
from features.constants import ClA_CONTACT_US_USER

@step(u'I select \'Contact us\' from the banner')
def step_impl(context):
    link = context.helperfunc.find_by_xpath("//span/a[text()='Contact us']")
    link.click()


@step(u'I select <question> from the contact civil legal advice page')
def step_impl(context):
    # Find the question by label
    # Find input and insert value from answer
    for row in context.table:
        label = row['question']
        checkbox = context.helperfunc.find_by_xpath(f"//div/label[contains(text(), '{label}')]")
        checkbox.click()


@step(u'I click \'continue to contact CLA\'')
def step_impl(context):
    context.execute_steps(u'''
        Given I click continue
    ''')


@step(u'I select \'Submit details\'')
def step_impl(context):
    context.execute_steps(u'''
        Given I click continue
    ''')


@step(u'I enter a name in the \'Your full name\' field')
def step_impl(context):
    value = ClA_CONTACT_US_USER
    full_name_input = context.helperfunc.find_by_xpath("//input[@id='full_name']")
    full_name_input.send_keys(value)
    assert full_name_input.get_attribute('value') == value


