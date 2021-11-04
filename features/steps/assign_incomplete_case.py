from behave import *
from selenium.webdriver.common.action_chains import ActionChains
from create_eligible_finances import create_eligible_finance


@given(u'case notes are empty')
def step_impl(context):
    notes = context.helperfunc.find_by_name('case.notes')
    assert len(notes.text) == 0


@step(u'I have created a user')
def step_impl(context):
    context.execute_steps(u'''
        When I select 'Create new user'
        And enter the client's personal details
        And I click the save button on the screen
    ''')


@given(u'I have created a valid discrimination scope')
def step_impl(context):
    context.execute_steps(u'''
        When I select ‘Create Scope Diagnosis'
        And I select the categories Discrimination, Direct Discrimination, Disability, Work
        Then I get an INSCOPE decision
        And select 'Create financial assessment'
    ''')


@given(u'I am on the Diversity tab')
def step_impl(context):
    create_eligible_finance(context)
    context.helperfunc.find_by_partial_link_text("Diversity").click()
    assert "Gender" in context.helperfunc.find_by_css_selector("h2[class='FormBlock-label ng-binding']").text


@when(u'I select \'Prefer not say\' for all diversity questions')
def step_impl(context):
    page = context.helperfunc
    radio = page.find_by_css_selector("input[name='gender'][value='Prefer not to say']")
    radio.click()
    page.find_by_name("diversity-next").click()

    assert "Ethnic origin" in page.find_by_css_selector("h2[class='FormBlock-label ng-binding']").text
    radio = page.find_by_css_selector("input[name='ethnicity'][value='Prefer not to say']")
    radio.click()
    page.find_by_name("diversity-next").click()

    assert "Disabilities" in page.find_by_css_selector("h2[class='FormBlock-label ng-binding']").text
    radio = page.find_by_css_selector("input[name='disability'][value='PNS - Prefer not to say']")
    radio.click()
    page.find_by_name("diversity-next").click()

    assert "Religion / belief" in page.find_by_css_selector("h2[class='FormBlock-label ng-binding']").text
    radio = page.find_by_css_selector("input[name='religion'][value='Prefer not to say']")
    radio.click()
    page.find_by_name("diversity-next").click()

    assert "Sexual orientation" in page.find_by_css_selector("h2[class='FormBlock-label ng-binding']").text
    radio = page.find_by_css_selector("input[name='sexual_orientation'][value='Prefer Not To Say']")
    radio.click()
    page.find_by_name("diversity-save").click()

    assert "The client has completed diversity monitoring." in page.find_by_class("SummaryBlock-content").text


@when(u'select the Assign tab')
def step_impl(context):
    context.helperfunc.find_by_partial_link_text("Assign").click()


@then(u'I get a message with the text "Case notes must be added to close a case"')
def step_impl(context):
    alert = context.helperfunc.find_by_css_selector("div[class='modal-dialog '")
    assert "Case notes must be added to close a case" in alert.text
