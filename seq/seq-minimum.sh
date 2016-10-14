#!/bin/sh
################################################################################
## \file      seq-minim.sh
## \author    SENOO, Ken
## \copyright CC0
################################################################################

set -u

seq()(
	readonly HELP_WARN="Try 'seq --help' for more information.\n"

	## Check arguments
	case $# in
		1) LAST="$1";;
		2) FIRST="$1" LAST="$2";;
		3) FIRST="$1" INCREMENT="$2" LAST="$3";;
		0) printf "seq: missing operand\n$HELP_WARN"    1>&2; exit 1;;
		*) printf "seq: extra operand '$4'\n$HELP_WARN" 1>&2; exit 1;;
	esac

	## Set default value
	: ${FIRST:=1} ${INCREMENT:=1} ${COMPARISON:=<}
	case "$INCREMENT" in -*) COMPARISON='>';; esac

	## Execute seq
	awk "BEGIN{for(i=$FIRST; i$COMPARISON=$LAST; i+=$INCREMENT) print i}"
)

seq "$@"
