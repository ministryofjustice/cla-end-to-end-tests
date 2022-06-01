# from features.steps.common_steps import wait_until_element_is_active
from features.constants import CLA_USER_TO_ASSIGN_CASES_TO


@given(u'a client with an existing case is added to it')
def step_impl(context):
    # you have to click on this div first to make everything else selectable
    select_user_div = context.helperfunc.find_by_id('s2id_searchPerson')
    select_user_div.click()
    # you then send the input to something other than the select2 box by clicking on a div/a first
    # you can then 'type' in the dropdown box and add text
    context.helperfunc.driver().switch_to.active_element.send_keys(CLA_USER_TO_ASSIGN_CASES_TO)
    # check that there are results and click on top value in dropdown
    # this element is not displayed until the user has typed in the search box
    # choose the first in the list and check the name of the person matches
    span_x_path = "//ul[@class='select2-results']/li/div/span"
    li_x_path = "//ul[@class='select2-results']/li"
    assert CLA_USER_TO_ASSIGN_CASES_TO == context.helperfunc.find_many_by_xpath(span_x_path)[0].text,  \
        f"Failed with {CLA_USER_TO_ASSIGN_CASES_TO} and {context.helperfunc.find_many_by_xpath(span_x_path)[0].text}"
    # select the first in the list
    context.helperfunc.find_many_by_xpath(li_x_path)[0].click()
    # there will be an alert asking if you wish to continue
    assert context.helperfunc.driver().switch_to.alert is not None, "No alert confirming you want to add the user"
    context.helperfunc.driver().switch_to.alert.accept()


