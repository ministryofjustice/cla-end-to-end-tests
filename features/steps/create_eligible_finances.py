from behave import *
from selenium.webdriver.common.action_chains import ActionChains

def create_eligible_finance(context):
    page = context.helperfunc
    # This has to be done after an inscope scope has been created
    # don't actually know if this a genuine profile, but gives you the
    # inscope scope
    page.find_by_partial_link_text("Finances").click()
    # selected_tab = context.helperfunc.find_by_css_selector("li[class='Pills-pill is-active']")
    # assert 'Details' in selected_tab.text
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

    # This clicks to the 'finance' tab ... in the finance tab. 
    finance_tab = page.find_by_xpath("//*[@id='pills-section-list']/li[2]")
    actions = ActionChains(page.driver())
    actions.move_to_element(finance_tab).perform()
    finance_tab.click()