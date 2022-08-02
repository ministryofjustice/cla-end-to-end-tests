from behave import *
from selenium.webdriver.common.by import By
import datetime
from selenium.webdriver.support.ui import WebDriverWait
import os
from features.constants import MINIMUM_WAIT_UNTIL_TIME, CLA_BACKEND_USER_TO_ASSIGN_STATUS_TO, CLA_BACKEND_USER_TO_ASSIGN_STATUS_TO_PK, FOX_ADMIN_NEW_OPERATOR
from features.steps.common_steps import wait_until_page_is_loaded, assert_header_on_page


@step(u'I enter a date range')
def step_impl(context):
    # report can only span 8 days
    # this can use the callbacks created for the other tests as all it does is check they are there
    # no concerns about order of tests running as it uses background task to create them if they are not there
    date_from = (datetime.datetime.now() + datetime.timedelta(days=-1)).strftime("%d/%m/%Y")
    date_to = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%d/%m/%Y")
    context.helperfunc.find_by_name("date_from").send_keys(date_from)
    context.helperfunc.find_by_name("date_to").send_keys(date_to)


@step(u'I select \'Export\'')
def step_impl(context):
    # no point checking for green message as it appears and stays even if this button clicked many times
    # but worth remembering how many rows in the table before we start
    xpath = "//div[@class='report-exports']/table/tbody/tr"
    # this will return an empty list if there is no table to be found
    context.how_many_reports_exist = len(context.helperfunc.driver().find_elements_by_xpath(xpath))
    context.helperfunc.click_button(By.NAME, "action")


@step(u'the report is processed and available to download as a .csv')
def step_impl(context):
    # check that there is a new line in the table for this export
    # wait until the row created
    xpath = "//div[@class='report-exports']/table/tbody/tr"

    class WaitForReportToBeCreated:
        def __init__(self, existing_no_reports):
            self._existing_reports = existing_no_reports

        def __call__(self, driver):
            #  need an extra row in the table and for that row to have "CREATED" and the link
            if len(context.helperfunc.driver().find_elements_by_xpath(xpath)) > 0:
                return (context.helperfunc.driver().find_elements_by_xpath(xpath)[-1].text.split(" ")[1] == "CREATED"
                        and len(context.helperfunc.driver().find_elements_by_xpath(xpath)) > self._existing_reports)
            else:
                return False

    wait = WebDriverWait(context.helperfunc.driver(), MINIMUM_WAIT_UNTIL_TIME)
    # need to wait until the file is created rather than just pending
    wait.until(WaitForReportToBeCreated(context.how_many_reports_exist), message='Report not created')


@step(u'I download the .csv')
def step_impl(context):
    # click on the link and download the csv, checking it has more than just a header
    class WaitForReportToBeDownloaded(object):
        def __init__(self, name):
            self._filename = name

        def __call__(self, driver):
            # find the file, open it and check that it has more than just the header
            if self._filename in os.listdir(context.download_dir):
                download_file_path = os.path.join(context.download_dir, self._filename)
                with open(download_file_path) as f:
                    num_lines = sum(1 for line in f)
                return num_lines > 1
            else:
                return False

    xpath = "//div[@class='report-exports']/table/tbody/tr"
    this_report = context.helperfunc.driver().find_elements_by_xpath(xpath)[-1].text.split(" ")
    href = this_report[2]
    xpath_a = f"{xpath}/td/a[@href='{href}']"
    file_name = context.helperfunc.driver().find_element_by_xpath(xpath_a).text.split("/")[-1]
    # click on the link
    context.helperfunc.driver().find_element_by_xpath(xpath_a).click()
    wait = WebDriverWait(context.helperfunc.driver(), MINIMUM_WAIT_UNTIL_TIME)
    str_error = f'No downloaded report for {file_name} in {context.download_dir}'
    wait.until(WaitForReportToBeDownloaded(file_name), message=str_error)


@step(u'I select a non-staff user from the list')
def step_impl(context):
    # just click on a user that we know has non-staff status
    context.execute_steps(f'''
    Given I select the link "{CLA_BACKEND_USER_TO_ASSIGN_STATUS_TO}"
    ''')


@when(u'I am taken to the user\'s details page')
def step_impl(context):
    # user details page is at /admin/auth/user/{pk}
    page = f"/admin/auth/user/{CLA_BACKEND_USER_TO_ASSIGN_STATUS_TO_PK}/"
    wait_until_page_is_loaded(page, context)
    assert_header_on_page("Change user", context)


@step(u'I select Staff status under permissions')
def step_impl(context):
    # click on the staff status checkbox
    xpath = f"//div[@class='checkbox-row']/input[@id='id_is_staff']"
    context.helperfunc.find_by_xpath(xpath).click()
    # for some reason this doesn't work
    # context.helperfunc.click_button(By.XPATH, xpath)


@step(u'I select save')
def step_impl(context):
    context.helperfunc.click_button(By.NAME, "_save")


@step(u'the users details are saved and I am taken back to the list of users')
def step_impl(context):
    # check that you have moved back to the list of users page
    page = f"/admin/auth/user/"
    wait_until_page_is_loaded(page, context)
    assert_header_on_page("Select user to change", context)
    # check there is a message that says the user was changed successfully
    link_text = 'The user "test_staff" was changed successfully'
    xpath = f"//ul/li[@class='success'][contains(text(), '{link_text}')]"
    assert len(context.helperfunc.find_many_by_xpath(xpath)) > 0, f"Cannot find success message"


@step(u'I choose to "{action}"')
def step_impl(context, action):
    if action == "Add operator":
        xpath = ".//li/a[@class='addlink']"
    elif action == "save":
        xpath = ".//input[@name='_save']"
    else:
        raise ValueError(f"Can not process this action. You entered {action}")
    # find the button and click it
    context.helperfunc.click_button(By.XPATH, xpath)


@step(u'I <provide> the <details> to create a user')
def step_impl(context):
    # Find the question by details
    # Find corresponding input and insert value from provide
    for row in context.table:
        text = row['details']
        value = row['provide']
        xpath = f".//label[text()='{text}']/following-sibling::input"
        context.helperfunc.find_by_xpath(xpath).send_keys(value)


@step(u'I select \'Is active’')
def step_impl(context):
    radio_input = context.helperfunc.find_by_css_selector(f"input[name='is_active']")
    radio_input.click()
    assert radio_input.get_attribute("checked") == "true"


@step(u'the new operator user is created')
def step_impl(context):
    # you are returned to the "select operator to change page"
    # the user just created exists
    # make sure that there are no errors on this page
    # are we still on the same page?
    if context.helperfunc.get_current_path() == "/admin/call_centre/operator/add/" and context.helperfunc.driver().find_element_by_xpath(f"//p[@class='errornote']") is not None:
        assert False, "There are errors creating that user"
    else:
        assert True


@step(u'I am taken to the list of operators page')
def step_impl(context):
    context.execute_steps('''
    Then I am taken to the "Select operator to change" page located on "/admin/call_centre/operator/"''')
    # the user just created exists - look for the created user in the table
    xpath = f".//table[@id='result_list']/tbody/tr[th/a[text()='{FOX_ADMIN_NEW_OPERATOR}']]"
    # .//table[@id='result_list']/tbody/tr[th/a[text()='elvis.presley']]
    assert context.helperfunc.find_by_xpath(xpath) is not None, f"cannot find row with user {FOX_ADMIN_NEW_OPERATOR}"
    # now check that it is active but not a manager or a superuser
    image_path_yes = "/static/admin/img/icon-yes.gif"
    image_path_no = "/static/admin/img/icon-no.gif"
    xpath_is_active = "//tr/td[@class='field-is_active_display']/img"
    xpath_is_manager = "//tr/td[@class='field-is_manager']/img"
    xpath_is_superuser = "//tr/td[@class='field-is_cla_superuser']/img"
    assert image_path_yes in context.helperfunc.find_by_xpath(xpath_is_active).get_attribute("src"),\
        f"User should be active"
    assert image_path_no in context.helperfunc.find_by_xpath(xpath_is_manager).get_attribute("src"), \
        f"User should not be manager"
    assert image_path_no in context.helperfunc.find_by_xpath(xpath_is_superuser).get_attribute("src"), \
        f"User should not be superuser"




