#!/bin/bash

# Simple wrapper for executing behave within Docker.

export A11Y=${A11Y_ENABLED:-false}
echo "A11Y is $A11Y"


exec behave "-D a11y=$A11Y"
# Clean up downloads
rm -rf data/downloads/*
