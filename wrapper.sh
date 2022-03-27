#!/bin/bash
set -Eeuo pipefail

echo "$@" >> /tmp/run.log
exec $@
