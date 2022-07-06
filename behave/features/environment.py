import os
import time
from behave.log_capture import capture
from features.constants import BROWSER, ARTIFACTS_DIRECTORY, DOWNLOAD_DIRECTORY
from helper.helper_web import get_browser


def before_all(context):
    # Reading the browser type from the configuration file
    helper_func = get_browser(BROWSER)
    context.helperfunc = helper_func
    # Dir to output test artifacts
    context.artifacts_dir = ARTIFACTS_DIRECTORY
    # dir for report fox_admin_downloads
    context.download_dir = DOWNLOAD_DIRECTORY
    helper_func.maximize()


@capture
def after_scenario(context, scenario):
    if scenario.status == 'failed':
        scenario_error_dir = os.path.join(context.artifacts_dir, 'feature_errors')
        make_dir(scenario_error_dir)
        scenario_file_path = os.path.join(scenario_error_dir, scenario.feature.name.replace(' ', '_')
                                          + '_' + time.strftime("%H%M%S_%d_%m_%Y")
                                          + '.png')
        context.helperfunc.take_screenshot(scenario_file_path)


def after_all(context):
    context.helperfunc.close()


def make_dir(dir):
    """
    Checks if directory exists, if not make a directory, given the directory path
    :param: <string>dir: Full path of directory to create
    """
    if not os.path.exists(dir):
        os.makedirs(dir)
