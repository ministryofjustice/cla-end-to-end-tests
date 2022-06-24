from behave import *


@step(u'I select \'Contact us\' from the banner')
def step_select_contact_us(context):
    link = context.helperfunc.find_by_xpath("//span/a[text()='Contact us']")
    link.click()


@step(u'I select <question> from the contact civil legal advice page')
def step_impl_means_test(context):
    # Find the question by label
    # Find input and insert value from answer
    for row in context.table:
        label = row['question']
        checkbox = context.helperfunc.find_by_xpath(f"//div/label[contains(text(), '{label}')]")
        checkbox.click()


@step(u'I click \'continue to contact CLA\'')
def step_click_submit(context):
    context.execute_steps(u'''
        Given I click continue
    ''')


@step(u'I am taken to the \'contact civil legal advice\' page')
def step_impl(context):
    assert context.helperfunc.find_by_xpath("//h1[contains(text(),'Contact Civil Legal Advice')]")
    current_path = context.helperfunc.get_current_path()
    assert current_path == "/contact", f"Current path is {current_path}. Expected /contact"
