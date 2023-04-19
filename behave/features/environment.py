import json
import os
import time
import logging
import subprocess

from axe_selenium_python import Axe
from behave.contrib.scenario_autoretry import patch_scenario_with_autoretry
from behave.log_capture import capture

from helper.constants import (
    BROWSER,
    DATA_DIRECTORY,
    A11Y_TAG,
    DATABASE_SNAPSHOT_ENABLED,
)

from helper.helper_web import get_browser
from features.steps.common_steps import check_accessibility, make_dir, get_tag


def before_all(context):
    context.feature_errors_dir = os.path.join(DATA_DIRECTORY, "feature_errors")
    make_dir(context.feature_errors_dir)
    context.download_dir = os.path.join(DATA_DIRECTORY, "downloads")
    make_dir(context.download_dir)
    context.a11y_reports_dir = os.path.join(DATA_DIRECTORY, "a11y_reports")
    make_dir(context.a11y_reports_dir)

    # Reading the browser type from the configuration file
    helper_func = get_browser(BROWSER, context.download_dir)
    context.helperfunc = helper_func
    # Boolean for axe finding a11y issues or not
    context.a11y_approved = True
    # Boolean that a11y environment variables are set
    a11y_arg = context.config.userdata.get("a11y", "false").lower() == "true"
    # Set userdata a11y to be boolean value and not a String
    context.config.userdata.update({"a11y": a11y_arg})
    helper_func.maximize()


def run_cmd(cmd):
    logging.info("running: %r" % cmd)
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate()
    if proc.returncode:
        logging.error(stderr)
    else:
        if stdout:
            logging.error("unexpected output: " + str(stdout))
        if stderr:
            logging.info(stderr)
    logging.info("done")


def restore_to_last_snapshot():
    cmd = [
        "pg_restore",
        "--clean",
        "--dbname=cla_backend",
        "cla_backend.backup",
    ]
    run_cmd(cmd)


def take_snapshot():
    cmd = [
        "pg_dump",
        "--clean",
        "--blobs",
        "--format=custom",
        "--file=cla_backend.backup",
        "--host=db",
        "--username=postgres",
    ]
    run_cmd(cmd)


def before_feature(context, feature):
    for scenario in feature.scenarios:
        patch_scenario_with_autoretry(scenario, max_attempts=3)


@capture
def before_scenario(context, scenario):
    if DATABASE_SNAPSHOT_ENABLED:
        take_snapshot()


@capture
def after_scenario(context, scenario):
    if not context.a11y_approved:
        logging.error("ACCESSIBILITY ISSUES FOUND, CHECK ARTIFACTS FOR INFORMATION")
    if scenario.status == "failed":

        if DATABASE_SNAPSHOT_ENABLED:
            restore_to_last_snapshot()

        scenario_file_path = os.path.join(
            context.feature_errors_dir,
            scenario.feature.name.replace(" ", "_")
            + "_"
            + time.strftime("%H%M%S_%d_%m_%Y")
            + ".png",
        )
        context.helperfunc.take_screenshot(scenario_file_path)


def after_all(context):
    f = open(f"{context.a11y_reports_dir}/a11y.json", "r")
    data = json.load(f)
    results_to_copy = []

    for index, error in enumerate(data):
        if index == 0:
            results_to_copy.append(error)
        else:
            contains_violation = False
            for issue in results_to_copy:
                if error["violations"] == issue["violations"]:
                    contains_violation = True
            if not contains_violation:
                results_to_copy.append(error)

    f = open(f"{context.a11y_reports_dir}/a11y_filtered.json", "x")
    axe = Axe(context.helperfunc.driver())
    axe.write_results(results_to_copy, f"{context.a11y_reports_dir}/a11y_filtered.json")
    f.close()
    context.helperfunc.close()


def after_step(context, step):
    # command to run: behave -D a11y=true -t @a11y-check
    if context.config.userdata["a11y"] and get_tag(context.tags, A11Y_TAG):
        # Returns False if a11y issues are found
        context.a11y_approved = check_accessibility(context, step.name)
