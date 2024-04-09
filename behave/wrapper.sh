#!/bin/bash

# Simple wrapper for executing behave within Docker.

export A11Y=${A11Y_ENABLED:-false}
echo "A11Y is $A11Y"

TAGS=""
# Run only FALA tagged tests
if [ "$FALA_TESTS_ONLY" = "true" ]
then
  TAGS="--tags=@fala"
fi
echo "TAGS is $TAGS"

#
# execute behave with flags
#

exec behave "-D a11y=$A11Y" $TAGS
# Clean up downloads
rm -rf data/downloads/*
