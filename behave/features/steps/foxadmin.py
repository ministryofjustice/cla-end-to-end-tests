from behave import *
from selenium.webdriver.common.by import By
import datetime
from selenium.webdriver.support.ui import WebDriverWait
import os
from features.constants import MINIMUM_WAIT_UNTIL_TIME


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




