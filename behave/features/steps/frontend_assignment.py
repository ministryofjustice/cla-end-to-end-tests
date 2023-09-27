from behave import step
import time
from helper.constants import (
    CLA_FRONTEND_PERSONAL_DETAILS_FORM_ALTERNATIVE_HELP,
    CLA_FRONTEND_PERSONAL_DETAILS_FORM,
    CLA_EXISTING_USER,
    MINIMUM_SLEEP_SECONDS,
    MATTER_TYPE_1,
    MATTER_TYPE_2,
    CLA_FRONTEND_URL,
    ASSIGN_F2F_CASE,
    CLA_FRONTEND_OOH_URL,
    CLA_SPECIALIST_PROVIDERS_NAME,
)
from selenium.webdriver.common.by import By
from common_steps import (
    click_on_hyperlink_and_get_href,
    switch_to_new_tab,
    select_value_from_list,
    search_and_select_case,
)
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException
from features.steps.common_steps import green_checkmark_appears_on_tab


@step("I complete the users details with {user_choice:w} details")
def step_impl_complete_user_details(context, user_choice):
    try:
        context.personal_details_form = (
            CLA_FRONTEND_PERSONAL_DETAILS_FORM_ALTERNATIVE_HELP[user_choice]
        )
    except KeyError:
        context.personal_details_form = CLA_FRONTEND_PERSONAL_DETAILS_FORM
    context.execute_steps(
        """
        When I select 'Create new user'
        And enter the client's personal details
        And I click the save button on the screen
    """
    )


@step("I navigate back to the call centre dashboard")
def step_impl_call_center_dashboard(context):
    url = f"{CLA_FRONTEND_URL}/call_centre/"
    context.helperfunc.open(url)


@step("I go back to the previous case")
def step_impl_back_to_prev_case(context):
    assert context.case_reference, "Context is missing case reference"
    url = f"{CLA_FRONTEND_URL}/call_centre/{context.case_reference}/diagnosis/"
    context.helperfunc.open(url)


@step("I see the users previously entered {user_choice:w} details")
def step_impl_previous_choice(context, user_choice):
    try:
        context.personal_details_form = (
            CLA_FRONTEND_PERSONAL_DETAILS_FORM_ALTERNATIVE_HELP[user_choice]
        )
    except KeyError:
        context.personal_details_form = CLA_FRONTEND_PERSONAL_DETAILS_FORM
    context.execute_steps(
        """
        Then I will see the users details
    """
    )


@step("I click on the Assign Alternative Help icon")
def step_impl_assign_alt_help(context):
    # no hyperlink text as it is just an icon in top RH corner
    x_path = ".//a[@title='Assign alternative help']"
    context.helperfunc.click_button(By.XPATH, x_path)


@step('I select "{face_to_face_text}" and I am taken to a new tab displaying FALA')
def step_impl_select_face_to_face(context, face_to_face_text):
    context.old_tabs = context.helperfunc.driver().window_handles
    last_hyperlink_selected = click_on_hyperlink_and_get_href(
        context, face_to_face_text
    )
    new_tabs = context.helperfunc.driver().window_handles
    for tab in new_tabs:
        if tab in context.old_tabs:
            pass
        else:
            new_tab = tab
    switch_to_new_tab(context, new_tab, last_hyperlink_selected)
    context.helperfunc.driver().switch_to.window(new_tab)
    # check the url
    assert last_hyperlink_selected == context.helperfunc.driver().current_url


@step("a Missing Information validation message is displayed to the user")
def step_impl_missing_info_validation(context):
    alert = context.helperfunc.find_by_css_selector("div[class='modal-dialog '")
    error_text = "You must collect at least a name and a postcode or phone number"
    assert error_text in alert.text


@step("a client with an existing case is added to it")
def step_impl_client_with_existing_case(context):
    select_value_from_list(
        context,
        label="Search for existing user",
        op="startswith",
        value=CLA_EXISTING_USER,
    )
    # there will be an alert asking if you wish to continue
    assert (
        context.helperfunc.driver().switch_to.alert is not None
    ), "No alert confirming you want to add the user"
    context.helperfunc.driver().switch_to.alert.accept()


@step("I select ‘Create Scope Diagnosis'")
def step_impl_select_create_scope(context):
    context.helperfunc.find_by_name("diagnosis-new").click()


@step("I select the diagnosis <category> and click next <number> times")
def step_impl_select_diagnosis_category(context):
    def wait_for_diagnosis_form(*args):
        form = context.helperfunc.find_by_name("diagnosis-form")
        return form is not None and form.is_displayed()

    wait = WebDriverWait(context.helperfunc.driver(), MINIMUM_SLEEP_SECONDS)
    wait.until(wait_for_diagnosis_form)

    # work out which category to choose
    # note that there is one category where have to click 'next' twice
    for row in context.table:
        category_text = row["category"]
        next_number = row["number"]
        # find the radio input next to the text of the category
        x_path = f".//p[contains(text(),'{category_text}')]//ancestor::label/input[@type='radio']"
        # for some reason these seem to return stale element errors
        context.helperfunc.click_button(By.XPATH, x_path)
        # now click next the correct number of times (normally 1)
        for _ in range(int(next_number)):
            context.helperfunc.click_button(By.NAME, "diagnosis-next")
            # This is required because the diagnosis-next button on the current page and next page have the same name
            # Without this sleep it will just find the same button and click it again instead of waiting for new button
            # to load
            time.sleep(MINIMUM_SLEEP_SECONDS)

    # Makes sure we at the end of the scope assessment
    # We can't rely on Finance tab being active as the scope could be out of scope

    def wait_for_diagnosis_delete_btn(*args):
        diagnosis_btn = context.helperfunc.find_by_name("diagnosis-delete")
        return diagnosis_btn is not None

    wait = WebDriverWait(context.helperfunc.driver(), 10)
    wait.until(wait_for_diagnosis_delete_btn)


@step('I get an "{scope}" decision')
def step_impl_scope_decision(context, scope):
    scope_xpath = (
        "//main/div[2]/div/div/div[3]/div/div[2]/div/div/form/section/div[5]/p"
    )

    scope_decision = context.helperfunc.find_by_xpath(scope_xpath)

    print(type(scope_decision))
    print(scope_decision)
    assert (
        scope in scope_decision.text
    ), f"The diagnosis form contained the following text: {scope_decision.text}, but did not find: {scope}"


@step('select the "{button_text}" button')
def step_impl_create_financial_assessment(context, button_text):
    context.helperfunc.find_by_partial_link_text(f"{button_text}").click()


@step('I am taken to the "{tab_name}" tab with the ‘Details’ sub-tab preselected')
@step('I remain in the "{tab_name}" tab')
def step_impl_finances_tab(context, tab_name):
    selected_tab = context.helperfunc.find_by_css_selector(
        "li[class='Tabs-tab is-active']"
    )
    assert tab_name in selected_tab.text


@step('I select the "{category}" knowledge base category')
def step_impl_select_category(context, category):
    select_value_from_list(context, label="Law category", value=category)
    # Need to wait for a bit for the ajax event to complete before continuing to the next step
    time.sleep(MINIMUM_SLEEP_SECONDS)


@step('I select the alternative help organisations "{organisation}"')
def step_impl_select_alt_help_org(context, organisation):
    name, _ = organisation.split(" - ")
    search_input = context.helperfunc.find_by_xpath(
        "//input[@placeholder='Search providers and other help organisations']"
    )
    search_input.clear()
    search_input.send_keys(name)
    submit = search_input.find_element_by_xpath("following-sibling::*")
    submit.click()
    # Need to wait for a bit for the ajax event to complete before continuing to the next step
    time.sleep(MINIMUM_SLEEP_SECONDS)
    search_results_form = context.helperfunc.find_by_xpath(
        '//form[@name="alternative_help"]'
    )
    # This will only find the first search result which is fine because we are searching for a specific organisation
    parent_wrapper = search_results_form.find_element_by_xpath(
        './/input[@name="selected_providers"]/ancestor::div[1]'
    )
    assert (
        parent_wrapper.find_element_by_css_selector(".FormRow-label strong").text
        == organisation
    )
    parent_wrapper.find_element_by_css_selector("label.FormRow-label").click()


@step('I enter "{comment}" in the Assignment comments box')
def step_impl_enter_assignment_comment(context, comment):
    text_area = context.helperfunc.find_by_xpath(
        '//textarea[@name="assign-notes"][@placeholder="Assignment comments"]'
    )
    text_area.send_keys(comment)
    assert text_area.get_attribute("value") == comment


@step("I click the Assign Alternative Help button")
def step_impl_click_assign_alt_help(context):
    submit_btn = context.helperfunc.find_by_xpath(
        '//button[@name="assign-alternative-help"]'
    )
    submit_btn.click()


@step("I am shown the survey reminder")
def step_impl_survey_reminder_shown(context):
    def wait_for_survey_reminder_dialog(*args):
        return context.helperfunc.find_by_css_selector(".modal-dialog") is not None

    wait = WebDriverWait(context.helperfunc.driver(), 10)
    wait.until(
        wait_for_survey_reminder_dialog, "Could not find survey reminder modal dialog"
    )
    heading = context.helperfunc.find_by_css_selector(
        ".modal-dialog .modal-content header h2"
    )
    assert heading.text == "Survey reminder"


@step("select continue on the survey reminder")
def step_impl_select_continue_on_survey(context):
    continue_btn = context.helperfunc.find_by_css_selector(
        ".modal-dialog .modal-content .FormActions button"
    )
    assert continue_btn.text == "Continue"
    continue_btn.click()


@step("case notes are empty")
def step_impl_empty_case_notes(context):
    notes = context.helperfunc.find_by_name("case.notes")
    assert len(notes.text) == 0


@step("I have created a user")
def step_impl_created_user(context):
    context.execute_steps(
        """
        When I select 'Create new user'
        And enter the client's personal details
        And I click the save button on the screen
    """
    )


@step("I have created a valid discrimination scope")
def step_impl_discrimination_scope(context):
    context.execute_steps(
        """
        When I select ‘Create Scope Diagnosis'
        And I select the diagnosis <category> and click next <number> times
        | category                                                | number |
        | Discrimination                                          | 2      |
        | Direct discrimination                                   | 1      |
        | Disability                                              | 1      |
        | Work                                                    | 1      |
        Then I get an "INSCOPE" decision
        And select the "Create financial assessment" button
    """
    )


@step("I am on the Diversity tab having answered the finances questions")
def step_impl_diversity_tab(context):
    def wait_until_finance_is_complete(*args):
        # this waits until all the finance questions have been answered
        classes = (
            context.helperfunc.find_by_css_selector("ul.Tabs")
            .find_element_by_link_text("Finances")
            .get_attribute("class")
        )
        return green_checkmark_appears_on_tab(classes)

    # first need to complete the finances tab
    context.execute_steps(
        """
        Given I am taken to the "Finances" tab with the ‘Details’ sub-tab preselected
        And I do not have a partner
        And I am aged 60 or over
        And I <answer> to Details <question>
          | question                                          | answer |
          | Universal credit                                  | No     |
          | Income Support                                    | No     |
          | Income-based Job Seekers Allowance                | No     |
          | Guarantee State Pension Credit                    | Yes    |
          | Income-related Employment and Support Allowance   | No     |
        Then I move onto Finances inner-tab
        And I <answer> to Finances <question>
          | question                                              | answer |
          | How much was in your bank account/building society    | 0.00   |
          | Do you have any investments, shares or ISAs?          | 0.00   |
          | Do you have any valuable items worth over £500 each?  | 0.00   |
          | Do you have any money owed to you?                    | 0.00   |
        And I select Save assessment
        And the 'Diversity' and 'Assign' tabs become available
    """
    )

    wait = WebDriverWait(context.helperfunc.driver(), 10)
    wait.until(wait_until_finance_is_complete)
    context.helperfunc.find_by_partial_link_text("Diversity").click()
    assert (
        "Gender"
        in context.helperfunc.find_by_css_selector(
            "h2[class='FormBlock-label ng-binding']"
        ).text
    )


@step("I select 'Prefer not say' for all diversity questions")
def step_impl_select_diversity_option(context):
    page = context.helperfunc
    radio = page.find_by_css_selector("input[name='gender'][value='Prefer not to say']")
    radio.click()
    page.find_by_name("diversity-next").click()

    radio = page.find_by_css_selector(
        "input[name='ethnicity'][value='Prefer not to say']"
    )
    assert (
        "Ethnic origin"
        in page.find_by_css_selector("h2[class='FormBlock-label ng-binding']").text
    )
    radio.click()
    page.find_by_name("diversity-next").click()
    # We need o either locate a new element that is not currently on the page
    # OR do an explicit wait, gone with find a new element that wasn't previously on the page
    radio = page.find_by_css_selector(
        "input[name='disability'][value='PNS - Prefer not to say']"
    )
    assert (
        "Disabilities"
        in page.find_by_css_selector("h2[class='FormBlock-label ng-binding']").text
    )
    radio.click()
    page.find_by_name("diversity-next").click()

    radio = page.find_by_css_selector(
        "input[name='religion'][value='Prefer not to say']"
    )
    assert (
        "Religion / belief"
        in page.find_by_css_selector("h2[class='FormBlock-label ng-binding']").text
    )
    radio.click()
    page.find_by_name("diversity-next").click()

    radio = page.find_by_css_selector(
        "input[name='sexual_orientation'][value='Prefer Not To Say']"
    )
    assert (
        "Sexual orientation"
        in page.find_by_css_selector("h2[class='FormBlock-label ng-binding']").text
    )
    radio.click()
    page.find_by_name("diversity-save").click()

    def wait_until_diversity_is_complete(*args):
        try:
            return (
                "The client has completed diversity monitoring."
                in page.find_by_class("SummaryBlock").text
            )
        except StaleElementReferenceException:
            return False

    wait = WebDriverWait(page.driver(), 10)
    wait.until(wait_until_diversity_is_complete)


@step("I select the Assign tab")
def step_impl_select_assign_tab(context):
    context.helperfunc.find_by_partial_link_text("Assign").click()


@step('I get a message with the text "Case notes must be added to close a case"')
def step_impl_case_notes_required(context):
    alert = context.helperfunc.find_by_css_selector("div[class='modal-dialog '")
    assert "Case notes must be added to close a case" in alert.text


@step('I enter the case notes "{case_notes_text}"')
def step_impl_case_notes(context, case_notes_text):
    notes = context.helperfunc.find_by_name("case.notes")
    # Focus on element first
    notes.click()
    notes.send_keys(case_notes_text)
    assert notes.get_attribute("value") == case_notes_text


@step("I select a category from Matter Type 1")
def step_impl_matter_type1(context):
    # Find matter type 1 wrapper and focus on it
    element = context.helperfunc.find_by_css_selector("#s2id_matter_type1")
    element.click()

    # Find an element by text
    context.helperfunc.find_by_xpath(f"//*[text()='{MATTER_TYPE_1}']").click()
    assert (
        element.find_element_by_css_selector("a .select2-chosen").text == MATTER_TYPE_1
    )


@step("I select a category from Matter Type 2")
def step_impl_matter_type2(context):
    # Find matter type 2 wrapper and focus on it
    element = context.helperfunc.find_by_css_selector("#s2id_matter_type2")
    element.click()

    # Find an element by text
    context.helperfunc.find_by_xpath(f"//*[text()='{MATTER_TYPE_2}']").click()
    assert (
        element.find_element_by_css_selector("a .select2-chosen").text == MATTER_TYPE_2
    )


@step("there is only one provider")
def step_impl_one_provider(context):
    form = context.helperfunc.find_by_name("assign_provider_form")

    # Providers are loaded via ajax after clicking the assign tab
    def wait_for_assign_providers_to_load(*args):
        return form.find_element_by_css_selector("div.ContactBlock") is not None

    wait = WebDriverWait(context.helperfunc.driver(), 10)
    wait.until(wait_for_assign_providers_to_load)

    # Find matter type 2 wrapper and focus on it
    headings = form.find_elements_by_css_selector("h2.ContactBlock-heading")
    context.provider_selected = headings[0].text
    assert len(headings) == 1


@step("I choose a provider")
def step_impl_choose_provider(context):
    form = context.helperfunc.find_by_name("assign_provider_form")

    # Providers are loaded via ajax after clicking the assign tab
    def wait_for_providers_to_load(*args):
        return form.find_element_by_css_selector("div.FormRow") is not None

    wait = WebDriverWait(context.helperfunc.driver(), 10)
    wait.until(wait_for_providers_to_load)

    # Find CLA_SPECIALIST_PROVIDERS_NAME and click on it
    # CLA_SPECIALIST_PROVIDERS_NAME may be the chosen provider
    # if not then we need to select one from the list below
    # if out of hours then there will be no "pre-selected provider"
    selected_provider_name = None
    if form.find_elements_by_css_selector(
        "div.ContactBlock ContactBlock--grey clearfix"
    ):
        selected_provider_name = form.find_elements_by_css_selector(
            "h2.ContactBlock-heading"
        )[0].text
    if not selected_provider_name == CLA_SPECIALIST_PROVIDERS_NAME:
        form.find_element_by_xpath(
            f""".//strong[@class='ng-binding'][text()='{CLA_SPECIALIST_PROVIDERS_NAME}']"""
        ).click()
    headings = form.find_elements_by_css_selector("h2.ContactBlock-heading")
    context.provider_selected = headings[0].text
    assert len(headings) == 1


@step("I select 'Assign Provider'")
def step_impl_assign_provider(context):
    context.case_id = context.helperfunc.find_by_css_selector(".CaseBar-caseNum a").text
    context.helperfunc.find_by_name("assign-provider").click()


@step("the case is assigned to the Specialist Provider")
def step_impl_case_assigned(context):
    def wait_until_case_is_assigned(*args):
        element = context.helperfunc.find_by_css_selector(
            ".NoticeContainer--fixed li.Notice"
        )
        return (
            element is not None
            and element.text
            == f"Case {context.case_id} assigned to {context.provider_selected}"
        )

    wait = WebDriverWait(context.helperfunc.driver(), 10)
    wait.until(wait_until_case_is_assigned)


@step("the case does not show up on the call centre dashboard")
def step_impl_case_removed_from_list(context):
    dashboard_url = f"{CLA_FRONTEND_URL}/call_centre/?ordering=-modified&page=1"
    context.helperfunc.open(dashboard_url)

    def wait_until_dashboard_page_is_loaded(*args):
        try:
            table = context.helperfunc.driver().find_element_by_css_selector(
                ".ListTable"
            )
            return context.case_id not in table.text
        except Exception:
            return False

    wait = WebDriverWait(context.helperfunc.driver(), 10)
    wait.until(wait_until_dashboard_page_is_loaded)


@step("the case does not show up on the call centre dashboard ooh")
def step_impl_case_removed_from_list_ooh(context):
    dashboard_url = f"{CLA_FRONTEND_OOH_URL}/call_centre/?ordering=-modified&page=1"
    context.helperfunc.open(dashboard_url)

    def wait_until_dashboard_page_is_loaded(*args):
        try:
            table = context.helperfunc.driver().find_element_by_css_selector(
                ".ListTable"
            )
            return context.case_id not in table.text
        except Exception:
            return False

    wait = WebDriverWait(context.helperfunc.driver(), 10)
    wait.until(wait_until_dashboard_page_is_loaded)


@step("I am on the Alternative Help page")
def step_impl_alt_help(context):
    # The case used has been created for this test case.
    # we select and then go through to alternative help
    search_and_select_case(context, ASSIGN_F2F_CASE)
    context.execute_steps(
        """
        When I click on the Assign Alternative Help icon
        Then I am taken to the "Alternative help" page for the case located at "/alternative_help/"
    """
    )


@step("I can select the Assign F2F button")
def step_impl_assign_f2f(context):
    # This clicks the face to face link, which is hidden as a tab.
    page = context.helperfunc
    tabs = page.find_by_css_selector("ul.Tabs")
    face_to_face_tab = tabs.find_element_by_link_text("Face to Face")
    page.driver().execute_script("arguments[0].click();", face_to_face_tab)
    # This clicks the actual assign F2F button.
    page.click_button(By.NAME, "assign-f2f")


@step('I select the "{option}" option and click next')
def step_impl_select_radio_button_option_by_value(context, option):
    value = ""
    if option == "Family":
        value = "n97"
    if option == "Special Guardianship Order":
        value = "n410"
    if option == "parent":
        value = "n411"
    if option == "other person":
        value = "n412"
    context.helperfunc.click_button(
        By.CSS_SELECTOR, f"input[type='radio'][value='{value}']"
    )
    context.helperfunc.click_button(By.NAME, "diagnosis-next")
