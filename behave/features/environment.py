import os
import time
from behave.contrib.scenario_autoretry import patch_scenario_with_autoretry
from behave.log_capture import capture
from helper.constants import (
    BROWSER,
    ARTIFACTS_DIRECTORY,
    DOWNLOAD_DIRECTORY,
    A11Y_TAG,
)
from helper.helper_web import get_browser
from features.steps.common_steps import check_accessibility, make_dir
import logging


def get_tag(context, find_tag):
    return [tag for tag in context if find_tag in tag]


def before_all(context):
    # Reading the browser type from the configuration file
    helper_func = get_browser(BROWSER)
    context.helperfunc = helper_func
    # Dir to output test artifacts
    context.artifacts_dir = ARTIFACTS_DIRECTORY
    # dir for report fox_admin_downloads
    context.download_dir = DOWNLOAD_DIRECTORY
    context.a11y = False
    helper_func.maximize()


def before_feature(context, feature):
    for scenario in feature.scenarios:
        patch_scenario_with_autoretry(scenario, max_attempts=3)


@capture
def after_scenario(context, scenario):
    if context.a11y:
        logging.error("ACCESSIBILITY ISSUES FOUND, CHECK ARTIFACTS FOR INFORMATION")
    if scenario.status == "failed":
        scenario_error_dir = os.path.join(context.artifacts_dir, "feature_errors")
        make_dir(scenario_error_dir)
        scenario_file_path = os.path.join(
            scenario_error_dir,
            scenario.feature.name.replace(" ", "_")
            + "_"
            + time.strftime("%H%M%S_%d_%m_%Y")
            + ".png",
        )
        context.helperfunc.take_screenshot(scenario_file_path)


def after_all(context):
    context.helperfunc.close()


# def before_step(context, step):
# Scenario.continue_after_failed_step = False


def after_step(context, step):
    try:
        # behave -D a11y=true -t @a11y-check
        if context.config.userdata["a11y"] == "true" and get_tag(
            context.tags, A11Y_TAG
        ):
            context.a11y = check_accessibility(context)
    except (KeyError, AttributeError):
        pass
