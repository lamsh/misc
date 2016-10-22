#!/bin/sh
# \file      is_option_enable.sh
# \author    SENOO, Ken
# \copyright CC0

set -u

is_option_enable()(
	: ${CMD:=$1} ${OPT:=$2}
	"$CMD" --help 2>&1 | grep -q -- "$OPT[=[, ]"
)

is_option_enable "$@"

## Test
# is_option_enable ls   --test        && echo "OK" || echo "NG"  # NG
# is_option_enable grep --exclude-dir && echo "OK" || echo "NG"  # OK
