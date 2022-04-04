#!/bin/sh
set -eu

# Poor man's sandbox for the compilers
# Functionality:
# - change to a non-root user
# - mask most non-essential environment variables (sudo does it by nature)
# Assumptions:
# - The file to be compiled is under working directory
# - No further directory structure
# - A end user cannot guess the path of another user's source code (no filesystem level isolation is implemented)
# Notes:
# - $PATH is fucked up (hardcoded in config.jd-compile.yaml), so we have to use only absolute path

# fix the permission: give write permission to the nobody user
/bin/chgrp --preserve-root --no-dereference -P --recursive nogroup -- .
/bin/chmod --preserve-root 0770 -- .
/bin/chmod --preserve-root 0660 -- ./*

/usr/bin/sudo -u nobody -g nogroup -- "$@"
