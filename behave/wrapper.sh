#!/bin/bash

# Simple wrapper for executing behave within Docker.

export DOCKER_BUILDKIT=1
export A11Y=${1:-false}

cd behave

exec behave "-D a11y=${A11Y}"