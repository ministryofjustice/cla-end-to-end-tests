#!/bin/bash

# Simple wrapper for executing behave within Docker.

export A11Y=${A11Y_ENABLED:-false}
echo "A11Y is $A11Y"


/usr/local/bin/python3 -c "import sys; print('Python:', sys.executable, sys.version); import pkg_resources; print('pkg_resources OK')" || echo "pkg_resources FAILED"
exec /usr/local/bin/python3 -m behave "-D a11y=$A11Y"
# Clean up downloads
rm -rf data/downloads/*
