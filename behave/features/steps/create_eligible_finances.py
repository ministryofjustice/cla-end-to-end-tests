from behave import *
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait

def create_eligible_finance(context):
    page = context.helperfunc
    tabs = page.find_by_css_selector("ul.Tabs")
    finance_tab_link = tabs.find_element_by_link_text("Finances")
    finance_tab_link.click()
    # This section is the 'Details' tab
    # click no to having a partner
    page.find_by_id("id_your_details-has_partner_1").click()
    # click yes to being over 60
    page.find_by_id("id_your_details-older_than_sixty_0").click()
    # click no to universal credit
    page.find_by_css_selector("input[name='your_details-specific_benefits-universal_credit'][value='false']").click()
    # click no to income support
    page.find_by_css_selector("input[name='your_details-specific_benefits-income_support'][value='false']").click()
    # click no job seekers allowance
    page.find_by_css_selector("input[name='your_details-specific_benefits-job_seekers_allowance'][value='false']").click()
    # click yes to receiving pension
    page.find_by_css_selector("input[name='your_details-specific_benefits-pension_credit'][value='true']").click()
    # click no to employment support
    page.find_by_css_selector("input[name='your_details-specific_benefits-employment_support'][value='false']").click()

    context.helperfunc.scroll_to_top()
    # This clicks to the 'finance' tab ... in the finance tab.
    finance_subtabs = page.find_by_css_selector(".Toolbar #pills-section-list")
    finance_subtabs.find_element_by_link_text("Finances").click()

    page.find_by_css_selector("input[ng-model='eligibility_check.you.savings.bank_balance']").send_keys('0')

    page.find_by_css_selector("input[ng-model='eligibility_check.you.savings.investment_balance']").send_keys('0')

    page.find_by_css_selector("input[ng-model='eligibility_check.you.savings.asset_balance']").send_keys('0')

    page.find_by_css_selector("input[ng-model='eligibility_check.you.savings.credit_balance']").send_keys('0')

    page.find_by_name("save-means-test").click()


    def wait_until_finance_is_complete(*args):
        classes = finance_tab_link.get_attribute("class")
        return "Icon--solidTick" in classes and "Icon--green" in classes
    wait = WebDriverWait(page.driver(), 10)
    wait.until(wait_until_finance_is_complete)


