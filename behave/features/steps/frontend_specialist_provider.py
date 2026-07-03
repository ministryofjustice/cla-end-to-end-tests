import os
from pathlib import Path
from behave import step
from helper.constants import (
    CLA_FRONTEND_URL,
    CLA_SPECIALIST_CASE_TO_ACCEPT,
    CLA_SPECIALIST_CASE_TO_REJECT,
    CLA_SPECIALIST_CASE_BANNER_BUTTONS,
    LOREM_IPSUM_STRING,
    CLA_SPECIALIST_REJECTION_OUTCOME_CODES,
    CLA_SPECIALIST_CASE_TO_SPLIT,
    CLA_SPECIALIST_CASE_TO_EDIT,
    CLA_SPECIALIST_SPLIT_CASE_RADIO_OPTIONS,
    CASE_SPLIT_TEXT,
    CLA_SPECIALIST_CSV_UPLOAD_PATH,
    CLA_SPECIALIST_CSV_UPLOAD_PATH_ERRORS,
    CLA_FRONTEND_CSV_URL,
    CLA_OPERATOR_CASE_TO_EDIT,
)
from features.steps.common_steps import (
    compare_client_details_with_backend,
    wait_until_page_is_loaded,
    green_checkmark_appears_on_tab,
    search_and_select_case,
)
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC


def _project_root_from_cwd(cwd):
    cwd_path = Path(cwd)
    if cwd_path.name == "behave":
        return cwd_path
    behave_path = cwd_path / "behave"
    if behave_path.exists():
        return behave_path
    return cwd_path


def _resolve_upload_file_path(relative_path):
    project_root = _project_root_from_cwd(os.getcwd())
    return str(project_root / relative_path.lstrip("/"))


@step("I am on the specialist provider cases dashboard page")
def step_on_spec_providers_dashboard(context):
    def wait_for_dashboard(*args):
        return context.helperfunc.find_by_css_selector("body.v-Dashboard") is not None

    wait = WebDriverWait(context.helperfunc.driver(), 10)
    wait.until(wait_for_dashboard, "Could not find dashboard")
    element = context.helperfunc.find_by_xpath("//html[@ng-app='cla.providerApp']")
    assert element is not None


@step("there is a case available")
def step_check_cases(context):
    # check there are cases available
    # only carry on if there are cases that have not been accepted
    x_path = ".//table[@class='ListTable']/tbody/tr/td/abbr[@title='Case status'][not(@class='Icon Icon--folderAccepted')]"
    cases_not_accepted = context.helperfunc.driver().find_elements(By.XPATH, x_path)
    assert len(cases_not_accepted) > 0, "No unaccepted cases"


@step("I can view the client details")
def step_impl_view_client_details(context):
    case_id = context.selected_case_ref
    client_section = context.helperfunc.find_by_id("personal_details")
    compare_client_details_with_backend(context, case_id, client_section)


@step('I select a "{case}" case from the dashboard')
def step_impl_select_case_from_specialist_dashboard(context, case):
    case_reference = get_case_reference(case)
    check_only_unaccepted_cases = False
    if case == "CLA_SPECIALIST_CASE_TO_ACCEPT":
        check_only_unaccepted_cases = True
    select_a_case(context, case_reference, check_only_unaccepted_cases)


def get_case_reference(case):
    case_dict = {
        "CLA_SPECIALIST_CASE_TO_EDIT": CLA_SPECIALIST_CASE_TO_EDIT,
        "CLA_SPECIALIST_CASE_TO_ACCEPT": CLA_SPECIALIST_CASE_TO_ACCEPT,
        "CLA_SPECIALIST_CASE_TO_REJECT": CLA_SPECIALIST_CASE_TO_REJECT,
        "CLA_SPECIALIST_CASE_TO_SPLIT": CLA_SPECIALIST_CASE_TO_SPLIT,
        "CLA_OPERATOR_CASE_TO_EDIT": CLA_OPERATOR_CASE_TO_EDIT,
    }
    return case_dict.get(case, None)


@step('I search for and select a "{case}" case')
def step_impl_search_and_select_case(context, case):
    # search_and_select_case sets context.selected_case_ref to CLA_OPERATOR_CASE_TO_EDIT
    case_ref = get_case_reference(case)
    search_and_select_case(context, case_ref)


@step("I search for and select a case using my saved reference number")
def step_impl_search_and_select_saved_case(context):
    # This test is dependent on `I save the reference number` step in order to work
    search_and_select_case(context, context.reference_number)


def select_a_case(context, case_reference, check_only_unaccepted_cases):
    table = context.helperfunc.find_by_css_selector(".ListTable")
    unaccepted_check = "unaccepted" if check_only_unaccepted_cases else ""
    # this will only return a link if the case hasn't already been accepted
    if check_only_unaccepted_cases:
        x_path = f".//tbody/tr[td/abbr[@title='Case status'][not(@class='Icon Icon--folderAccepted')]]/td/a[text()='{case_reference}']"
    else:
        x_path = f".//tbody/tr[td/abbr[@title='Case status']]/td/a[text()='{case_reference}']"
    try:
        link = table.find_element(By.XPATH, x_path)
        assert (
            link is not None
        ), f"Could not find {unaccepted_check} case {case_reference} on the dashboard"
        assert (
            link.text == case_reference
        ), f"Expected: {case_reference} - Found: {link.text}"
    except NoSuchElementException:
        assert (
            False
        ), f"Could not find {unaccepted_check} case {case_reference} on the dashboard"
    context.selected_case_ref = case_reference
    link.click()


@step("I can view the case details and notes entered by the Operator")
def step_impl_view_operator_case_details(context):
    # check there is a case history on the rhs
    case_history = context.helperfunc.find_by_class("CaseHistory")
    assert case_history is not None
    # check that there are operator comments
    operator_comments = context.helperfunc.find_by_class("CommentBlock").find_elements(
        By.XPATH, "./child::*"
    )
    # "operator said" is the second child and then there are case notes below that.
    assert len(operator_comments) >= 3


@step("I select Scope")
def step_impl_select_scope(context):
    scope_link = context.helperfunc.find_by_xpath(
        '//a[@ui-sref="case_detail.edit.diagnosis"]'
    )
    assert scope_link is not None
    # click on the link
    scope_link.click()


@step("I can view the scope assessment entered by the Operator")
def step_impl_view_scope_assessment(context):
    # <section class="SummaryBlock SummaryBlock--compact ng-scope" ng-if="diagnosis.nodes">
    # check that the scope assessment exists
    scope_description = context.helperfunc.find_by_xpath(
        '//section[@class="SummaryBlock SummaryBlock--compact ng-scope"]'
    )
    assert scope_description is not None
    # check that there is a category of law and that it is INSCOPE
    scope_inscope = scope_description.find_elements(
        By.XPATH, './/div/p[text()="INSCOPE"]'
    )
    assert scope_inscope is not None
    # scope_descriptors = scope_description.find_element(By.XPATH, f'.//div/p')
    scope_cat_of_law = scope_description.find_element(
        By.XPATH, './/div/p[starts-with(.,"Category of law")]'
    )
    assert scope_cat_of_law is not None and len(scope_cat_of_law.text) > len(
        "Category of law:"
    )


@step("I select '{value}' in the case details page")
def step_impl_select_value(context, value):
    # Using python dictionary to find name value for accept, reject and split
    xpath = f"//button[@name='{CLA_SPECIALIST_CASE_BANNER_BUTTONS[value]}']"
    context.helperfunc.click_button(By.XPATH, xpath)


@step("I accept the case and open the Legal Help Form")
def step_impl_select_case_and_legal_help_form(context):
    # If same case is being used to test different outcomes after being accepted.
    # Then ignore the accept button is missing and just go to the legal help form.
    try:
        # By using find_element_by_xpath, NoSuchElementException can be raised if not found.
        context.case_details = context.helperfunc.find_by_xpath("//*[@id='wrapper']")
        accept_button = context.case_details.find_element(
            By.XPATH,
            f"//button[@name='" f"{CLA_SPECIALIST_CASE_BANNER_BUTTONS['Accept']}']",
        )
        accept_button.click()
        find_help_form_link(context)
    except NoSuchElementException:
        find_help_form_link(context)


def find_help_form_link(context):
    locators = [
        (By.XPATH, "//a[contains(normalize-space(.), 'Legal help form')]"),
        (By.PARTIAL_LINK_TEXT, "Legal help form"),
    ]

    for by, selector in locators:
        try:
            legal_help_link = WebDriverWait(context.helperfunc.driver(), 15).until(
                EC.presence_of_element_located((by, selector))
            )
            href = legal_help_link.get_attribute("href")
            try:
                context.helperfunc.click_button(by, selector)
                return
            except TimeoutException:
                if href:
                    context.helperfunc.open(href)
                    return
        except TimeoutException:
            continue

    assert False, "Could not find legal help form link"


@step('I select the "{value}" tab on the specialist provider case page')
def step_impl_finance_tab_specialist_provider(context, value):
    # Another way to select the pages tabs as HTML is different on specialist provider case page.
    xpath = f"//a[contains(text(), '{value}')]"
    context.helperfunc.click_button(By.XPATH, xpath)


@step("I can see a 'Case accepted successfully' message")
def step_impl_case_accepted(context):
    # wait for the flash message to appear.
    flash_message = context.helperfunc.find_by_xpath(
        '//*[text()="Case accepted successfully"]'
    )
    assert flash_message is not None


@step("I return to the specialist provider cases dashboard page")
def step_impl_return_to_dashboard(context):
    # click on the 'back to cases' link
    back_to_cases = context.helperfunc.find_by_xpath(
        '//a[@class="SubNav-link SubNav-link--back"]'
    )
    assert back_to_cases is not None
    back_to_cases.click()


@step("I select the Accepted tab")
def step_impl_select_accepted(context):
    # click on the 'Accepted' tab
    accepted_tab = context.helperfunc.find_by_xpath(
        '//a[@class="Label Icon Icon--folderAccepted"]'
    )
    assert accepted_tab is not None
    accepted_tab.click()


@step("I can see my accepted case reference number")
def step_impl_view_reference_number(context):
    # click on the 'back to cases' link
    my_case = context.helperfunc.find_by_xpath(
        f"//*[text()='{context.selected_case_ref}']"
    )
    assert my_case is not None


@step("I am viewing a case that I have accepted as a specialist provider")
def step_impl_view_accepted_case(context):
    case_reference = CLA_SPECIALIST_CASE_TO_ACCEPT
    # reset the case context here as it is used in lots of places, need to make sure we have the one we want
    context.selected_case_ref = case_reference
    login_url = f"{CLA_FRONTEND_URL}/provider/{case_reference}/diagnosis/"
    context.helperfunc.open(login_url)


@step("I select the Legal help form")
def step_impl_select_legl_help(context):
    find_help_form_link(context)


def assert_your_details(table, root_element):
    for row in table:
        label_element = root_element.find_element(
            By.XPATH, f".//*[text()='{row['field']}']"
        )
        assert (
            label_element is not None
        ), f"Could not find question on legal help form: {row['field']}"
        parent_element = label_element.find_element(By.XPATH, "./..")
        try:
            value_element = parent_element.find_element(By.TAG_NAME, "input")
        except NoSuchElementException:
            value_element = parent_element.find_element(By.TAG_NAME, "textarea")

        assert (
            value_element is not None
        ), f"Could not find value for question: {row['field']}"

        expected_label = row["field"].upper()
        expected_value = row["value"].upper()
        actual_value = value_element.get_attribute("value").upper()
        actual_label = label_element.text.upper()

        assert (
            actual_label == expected_label
        ), f"Expected label: {expected_label} - Actual value:{actual_label}"
        assert (
            actual_value == expected_value
        ), f"Expected value: {expected_value} - Actual value:{actual_value}"


def assert_four_column_table(table, root_element):
    QUESTION_COL_KEY = 0
    COL_TWO_KEY = 1
    COL_THREE_KEY = 2
    COL_FOUR_KEY = 3

    def get_cell_value(cell_element):
        # The legal help table can render values as inputs or plain text cells.
        form_controls = cell_element.find_elements(
            By.CSS_SELECTOR, "input, textarea, select"
        )
        if form_controls:
            control = form_controls[0]
            if control.tag_name.lower() == "select":
                return Select(control).first_selected_option.text.strip()
            value = control.get_attribute("value")
            if value is not None:
                return value.strip()
        return cell_element.text.strip()

    def assert_cell(cell_element, question, expected_value):
        value = get_cell_value(cell_element)
        assert (
            value == expected_value.strip()
        ), f"Question: {question} - Expected: {expected_value} - Actual: {value}"

    for row in table:
        question = row[QUESTION_COL_KEY]
        label_element = root_element.find_element(
            By.XPATH, f".//*[normalize-space(text())='{question}']"
        )
        assert (
            label_element is not None
        ), f"Could not find question on legal help form: {question}"
        parent_element = label_element.find_element(By.XPATH, "./ancestor::tr[1]")
        elements = parent_element.find_elements(By.CSS_SELECTOR, "td")
        assert len(elements) > 1, f"No value cells found for question: {question}"

        assert_cell(elements[1], question, row[COL_TWO_KEY])
        if len(row) > 2 and row[COL_THREE_KEY].lower() != "n/a":
            assert len(elements) > 2, (
                f"Expected partner/second column for question: {question}"
            )
            assert_cell(elements[2], question, row[COL_THREE_KEY])
        if len(row) > 3 and row[COL_FOUR_KEY].lower() != "n/a":
            assert len(elements) > 3, (
                f"Expected third value column for question: {question}"
            )
            assert_cell(elements[3], question, row[COL_FOUR_KEY])


@step("The legal help form Your Details section has the values")
def step_impl_your_details_values(context):
    driver = context.helperfunc.driver()
    heading_element = driver.find_element(By.XPATH, "//h2[text()='Your Details']")
    wrapper_element = heading_element.find_element(By.XPATH, "./..")
    assert_your_details(context.table, wrapper_element)


@step('The legal help form "{section_heading}" section has the values')
def step_impl_legal_help_values(context, section_heading):
    driver = context.helperfunc.driver()
    heading_element = driver.find_element(By.XPATH, f"//h2[text()='{section_heading}']")
    wrapper_element = heading_element.find_element(By.XPATH, "./..")
    assert_four_column_table(context.table, wrapper_element)


@step(
    "The legal help form Your Income section (less Monthly allowances) has the values"
)
def step_impl_income_values(context):
    driver = context.helperfunc.driver()
    heading_element = driver.find_element(By.XPATH, "//h2[text()='Your Income']")
    wrapper_element = heading_element.find_element(By.XPATH, "./..")
    sub_heading_element = wrapper_element.find_element(
        By.XPATH, ".//*[text()='Less monthly allowances']"
    )
    wrapper_element = sub_heading_element.find_element(
        By.XPATH, "./..//ancestor::table"
    )
    assert_four_column_table(context.table, wrapper_element)


@step("I select Finances")
def step_impl_select_finances(context):
    tabs = context.helperfunc.find_by_css_selector("ul.Tabs")
    finance_tab_link = tabs.find_element(By.LINK_TEXT, "Finances")
    assert finance_tab_link is not None

    # click on the link
    finance_tab_link.click()


@step("I can view the financial assessment entered by the Operator")
def step_impl_view_financial_assessment(context):
    classes = (
        context.helperfunc.find_by_css_selector("ul.Tabs")
        .find_element(By.LINK_TEXT, "Finances")
        .get_attribute("class")
    )
    # Checking that the green tick is present for having the finance previously completed.
    assert green_checkmark_appears_on_tab(classes) is True
    # Checking that the overall form has loaded by checking one of the elements are there.
    assert context.helperfunc.find_by_id("id_your_details-has_partner_1") is not None


@step("the reject modal appears on screen")
def step_impl_reject_modal(context):
    def wait_for_reject_dialog(*args):
        return context.helperfunc.find_by_css_selector(".modal-dialog") is not None

    wait = WebDriverWait(context.helperfunc.driver(), 10)
    wait.until(wait_for_reject_dialog, "Could not find reject modal dialog")
    heading = context.helperfunc.find_by_css_selector(
        ".modal-dialog .modal-content header h2"
    )
    assert heading.text == "Reject case"


@step("the split case modal appears on screen")
def step_impl_split_case_modal(context):
    def wait_for_reject_dialog(*args):
        return context.helperfunc.find_by_css_selector(".modal-dialog") is not None

    wait = WebDriverWait(context.helperfunc.driver(), 10)
    wait.until(wait_for_reject_dialog, "Could not find split case modal dialog")
    heading = context.helperfunc.find_by_css_selector(
        ".modal-dialog .modal-content header h2"
    )
    assert heading.text == f"Split case {CLA_SPECIALIST_CASE_TO_SPLIT}"


@step("I select a reject reason of '{reject_reason}'")
def step_impl_select_reject_reason(context, reject_reason):
    context.modal = context.helperfunc.find_by_css_selector(".modal-dialog")
    modal_input = context.modal.find_element(
        By.XPATH, f"//input[@value='{reject_reason}']"
    )
    assert modal_input is not None
    modal_input.click()


@step("I enter a reason into the Notes textarea")
def step_impl_enter_reason(context):
    context.modal = context.helperfunc.find_by_css_selector(".modal-dialog")
    comment = LOREM_IPSUM_STRING
    text_area = context.modal.find_element(
        By.XPATH, '//textarea[@name="outcomeNotes"][@placeholder="Notes"]'
    )
    text_area.send_keys(comment)
    assert text_area.get_attribute("value") == comment


@step("I confirm that my case has an Outcome code of '{reject_reason}'")
def step_impl_confirm_outcome_code(context, reject_reason):
    outcome_code = context.helperfunc.find_by_xpath(
        f"//abbr[@title='" f"{CLA_SPECIALIST_REJECTION_OUTCOME_CODES[reject_reason]}']"
    )
    assert outcome_code is not None
    assert (
        outcome_code.get_attribute("title")
        == CLA_SPECIALIST_REJECTION_OUTCOME_CODES[reject_reason]
    )


@step("the 'New case' drop down values are")
def step_impl_new_case_dropdown(context):
    # Find the modal container
    context.modal = context.helperfunc.find_by_css_selector(".modal-dialog")
    # Inside modal find the form we want to focus on.
    context.form = context.modal.find_element(
        By.XPATH, "//form[@name='split_case_frm']"
    )
    for row in context.table:
        label = row["label"]
        value = row["value"]

        label_link = context.form.find_element(
            By.XPATH, f"//span[text()='{label}']/../../span/span/div/a"
        )
        # Clicking this link will automatically focus the input for us to type into
        label_link.click()

        def wait_for_list_of_values(*args):
            try:
                # Try and see when this element is visible in the modal
                context.form.find_element(By.XPATH, f"//li/div[text()='{value}']")
                return True
            except NoSuchElementException:
                return False

        wait = WebDriverWait(context.helperfunc.driver(), 10)
        wait.until(
            wait_for_list_of_values,
            message=f"Could not find any matches for {value} in {label} list",
        )
        list_item = context.form.find_element(By.XPATH, f"//li/div[text()='{value}']")
        list_item.click()

        # Once list item has been selected, check the anchor contains the correct value
        label_value = context.form.find_element(
            By.XPATH,
            f"//span[text()='{label}']"
            f"/../../span/span/div/a/span[text()='{value}']",
        )
        assert label_value.text == value


@step("I enter a comment into the new case notes textarea")
def step_impl_enter_comment(context):
    context.modal = context.helperfunc.find_by_css_selector(".modal-dialog")
    comment = CASE_SPLIT_TEXT
    text_area = context.modal.find_element(
        By.XPATH, '//textarea[@name="notes"][@placeholder="Enter comments"]'
    )
    text_area.send_keys(comment)
    assert text_area.get_attribute("value") == comment


@step("I select '{value}' for the 'Assign' radio options")
def step_impl_select_assign(context, value):
    context.modal = context.helperfunc.find_by_css_selector(".modal-dialog")
    modal_input = context.modal.find_element(
        By.XPATH,
        f"//input[@value=" f"'{CLA_SPECIALIST_SPLIT_CASE_RADIO_OPTIONS[value]}']",
    )
    assert modal_input is not None
    modal_input.click()


@step("the new split case is available to the operator")
def step_impl_split_case(context):
    # Goto to the dashboard ordered by latest
    context.helperfunc.open(f"{CLA_FRONTEND_URL}/call_centre/?ordering=-modified")
    table = context.helperfunc.find_by_css_selector(".ListTable")
    # Find the case on the dashboard and navigate to it
    case_ref = table.find_element(By.XPATH, ".//tbody/tr/td[2]/a").text
    context.helperfunc.open(f"{CLA_FRONTEND_URL}/call_centre/{case_ref}")
    # Find the comment identifying that this case was split from our known case
    full_case_log = context.helperfunc.find_by_css_selector(".CaseHistory-log").text
    assert (
        CASE_SPLIT_TEXT in full_case_log
    ), "Could not find split case in operators dashboard"


@step("I am on the CSV upload page")
def step_impl_csv_upload_page(context):
    csv_page = f"{CLA_FRONTEND_URL}{CLA_FRONTEND_CSV_URL}"
    context.helperfunc.open(csv_page)
    page = CLA_FRONTEND_CSV_URL
    wait_until_page_is_loaded(page, context)
    header = context.helperfunc.find_by_xpath("//header/h2[text()='CSV Upload']")
    assert header is not None


@step("I select 'Choose file' and upload an {csv_option} csv file")
def step_impl_choose_upload_file(context, csv_option):
    input_csv = context.helperfunc.find_by_xpath("//input[@name='csvfile']")
    if csv_option == "valid":
        input_csv.send_keys(_resolve_upload_file_path(CLA_SPECIALIST_CSV_UPLOAD_PATH))
    elif csv_option == "invalid":
        input_csv.send_keys(
            _resolve_upload_file_path(CLA_SPECIALIST_CSV_UPLOAD_PATH_ERRORS)
        )
    else:
        assert (
            False
        ), "You did not provide the correct String value, must be string value valid or invalid"


@step("I select the month and year for the uploaded csv file")
def step_impl_select_date_for_upload(context):
    # Alter date to be the first day of month
    # Minis one month because current month will not be visible as option
    new_date = context.helperfunc.date_start_this_month.strftime("%Y-%m-%d")
    select = Select(
        context.helperfunc.find_by_xpath('//form[@name="csvForm"]/label/select')
    )
    assert select is not None
    try:
        select.select_by_value(f"string:{new_date}")
    except StaleElementReferenceException:
        # Note: always check generated screenshot to ensure that select option is visible and functioning
        assert False, f"Could not find {new_date} in select options"


@step("I select the 'Upload' button")
def step_impl_select_upload(context):
    button = context.helperfunc.find_by_xpath(
        "//button[@type='submit'][text()='Upload']"
    )
    assert button is not None
    button.click()


@step("I check that there are no errors in the csv upload page")
def step_impl_no_csv_errors(context):
    # A notice can indicate success or failure. Only fail on error-like notice text.
    notice_texts = [
        notice.text.strip().lower()
        for notice in context.helperfunc.driver().find_elements(
            By.CSS_SELECTOR, ".Notice--closeable"
        )
        if notice.text.strip()
    ]

    error_notice_fragments = ["error", "already", "invalid", "problem", "failed"]
    has_error_notice = any(
        any(fragment in text for fragment in error_notice_fragments)
        for text in notice_texts
    )
    assert not has_error_notice, (
        "Errors were found in the CSV Upload page notice: " f"{notice_texts}"
    )

    # If you upload a CSV file that has problems with some of its rows, a dynamic HTML element
    # appears in the DOM with a list of the following errors for the user to address.
    try:
        WebDriverWait(context.helperfunc.driver(), 5).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".ErrorSummary-list"))
        )
        assert False, "Errors were found in the CSV Upload page header."
    except TimeoutException:
        pass


@step("I can see the file listed in the uploaded files table")
def step_impl_uploaded_file_list(context):
    # Create a string that is a short version of the month and year only
    new_date = context.helperfunc.date_start_this_month.strftime("%b %Y")
    # Find the same date as the uploaded csv file
    table_row = context.helperfunc.find_by_xpath(
        f"//table/tbody/tr/td[contains(text(), '{new_date}') and contains(text(), 'Upload')]"
    )
    assert table_row is not None


@step("I am given details of the errors in each line of the csv file")
def step_impl_csv_error_details(context):
    context.csv_page = context.helperfunc.find_by_xpath("//*[@id='wrapper']")
    # Wait for error rows to render after upload submission.
    xpath = "//ul[contains(@class, 'ErrorSummary-list')]/li"
    WebDriverWait(context.helperfunc.driver(), 10).until(
        lambda _driver: len(context.helperfunc.driver().find_elements(By.XPATH, xpath))
        > 0
        or len(
            context.helperfunc.driver().find_elements(
                By.CSS_SELECTOR, ".Notice--closeable"
            )
        )
        > 0,
        message="No CSV validation errors were rendered on the upload page",
    )

    error_list = context.helperfunc.driver().find_elements(By.XPATH, xpath)
    if len(error_list) == 0:
        notice_text = context.helperfunc.driver().find_elements(
            By.CSS_SELECTOR, ".Notice--closeable"
        )
        rendered_notices = [n.text.strip() for n in notice_text if n.text.strip()]
        assert (
            False
        ), f"Expected line-level CSV errors but found notices instead: {rendered_notices}"

    # Loop through HTML li elements and make sure the list items contain text.
    for error_item in error_list:
        error_text = error_item.get_attribute("innerText")
        assert error_text is not None and error_text.strip() != ""


@step("I can see on Finances inner-tab <question> that the <answer> remain updated")
def step_impl_your_finances_values(context):
    for row in context.table:
        label = row["question"]
        value = row["answer"]
        label_format = label.ljust(len(label) + 1)
        assert value == context.helperfunc.find_by_xpath(
            f"//span[contains(text(),'{label_format}')]/../input"
        ).get_attribute("value")
