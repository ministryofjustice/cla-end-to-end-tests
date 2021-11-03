from behave import *


def set_input_field_by_label(context, label, value):
    context.helperfunc.find_by_xpath(f"//span[text()='{label}']/../input").send_keys(value)