#!/bin/bash
#
# Simple wrapper for executing behave within Docker.
#
# ENVIRONMENT VARIABLES:
#
#    - REQUIREMENTS_PATH: requirements fullpath;
#          default = "features/steps/requirements.txt"
#


#
# execute behave
#
cd behave

exec behave "$@"