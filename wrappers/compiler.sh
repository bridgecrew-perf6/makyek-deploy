#!/bin/sh

# Functionality:
# - change to a non-root user
# - mask most non-essential environment variables (sudo does it by nature)
# Assumptions:
# - The file to be compiled is under working directory
# - No further directory structure
# - A end user cannot guess the path of another user's source code (no filesystem level isolation is implemented)

# fix the permission: give write permission to the nobody user
chgrp --perserve-root --no-dereference --verbose -P nogroup -- .
chmod --preserve-root --verbose 0770 -- .
chmod --preserve-root --verbose 0660 -- ./*

sudo -u nobody -- "$@"
