from selenium.webdriver.support.wait import WebDriverWait

# These tests will reuse lots of the steps from the discrimination diagnosis P1 cases
@given(u'a client with an existing case is added to it')
def step_impl(context):
    # first get the name of the existing client
    # TODO will use name in LGA-1835 - will eventually point to variable in constants.py
    CLA_USER_TO_ASSIGN_CASES_TO = "John Smith"
    # now put this into the 'choose a user' box.
    # you have to click on this div first to make everything else selectable
    select_user_div = context.helperfunc.find_by_id('s2id_searchPerson')
    select_user_div.click()
    # you then send the input to something other than the select2 box by clicking on a div/a first
    # you can then 'type' in the dropdown box and add text
    input_user_search = context.helperfunc.find_by_xpath("//div[@id='s2id_searchPerson']/a")
    assert input_user_search is not None
    input_user_search.send_keys(CLA_USER_TO_ASSIGN_CASES_TO)
    # check that there are results and click on top value in dropdown
    # this element is not displayed until the user has typed in the search box
    # choose the first in the list and check the name of the person matches
    span_x_path = "//ul[@class='select2-results']/li/div/span"
    li_x_path = "//ul[@class='select2-results']/li"
    assert CLA_USER_TO_ASSIGN_CASES_TO == context.helperfunc.find_many_by_xpath(span_x_path)[0].text
    # select the first in the list
    context.helperfunc.find_many_by_xpath(li_x_path)[0].click()

