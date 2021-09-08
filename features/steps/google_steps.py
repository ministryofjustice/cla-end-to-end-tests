from behave import *


@given(u'I am on the Google search page')
def step_impl(context):
    # Opens google.com
    context.helperfunc.open('http://www.google.com')
    # this clicks agree on a cookies warning
    context.helperfunc.find_by_xpath('//*[@id="L2AGLb"]/div').click()


@when(u'I search \'ministry of justice\'')
def step_impl(context):
    # enters the search term
    context.helperfunc.find_by_xpath('/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys("ministry of justice")
    # this submits the form, you could also search for the submit button and click that if 
    # you want
    context.helperfunc.find_by_xpath('/html/body/div[1]/div[3]/form').submit()
    

@then(u'I can see many results.')
def step_impl(context):
    # This checks to see if a ministry of justice link appears on the page
    context.helperfunc.find_by_partial_link_text('Ministry of Justice')
