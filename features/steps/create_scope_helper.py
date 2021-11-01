from behave import *


def create_valid_discrimination_scope(context):
    # You have to be on the case details page for this
    context.helperfunc.find_by_name("diagnosis-new").click()

    form = context.helperfunc.find_by_name('diagnosis-form')
    assert form.is_displayed()

    # Discrimination
    context.helperfunc.find_by_xpath("//input[@value='n106']").click()
    context.helperfunc.find_by_name("diagnosis-next").click()
    assert context.helperfunc.find_by_class("SummaryBlock-node-n106").is_displayed()
    
    # Just clicking next
    context.helperfunc.find_by_name("diagnosis-next").click()

    # Direct discrimination
    context.helperfunc.find_by_xpath("//input[@value='n108']").click()
    context.helperfunc.find_by_name("diagnosis-next").click()

    # Disability
    context.helperfunc.find_by_xpath("//input[@value='n109']").click()
    context.helperfunc.find_by_name("diagnosis-next").click()

    # Work
    context.helperfunc.find_by_xpath("//input[@value='n110']").click()
    context.helperfunc.find_by_name("diagnosis-next").click()
    
    # Makes sure we at the end of the scope assessment
    assert context.helperfunc.find_by_partial_link_text('Create financial assessment').is_displayed()

    context.helperfunc.find_by_partial_link_text('Create financial assessment').click()

    selected_tab = context.helperfunc.find_by_css_selector("li[class='Tabs-tab is-active']")
    assert 'Finances' in selected_tab.text