#!/bin/sh
################################################################################
## \file      parse_arg_for.sh
## \author    SENOO, Ken
## \copyright CC0
## \date      first created date: 2017-01-11T23:36+09:00
## \date      last  updated date: 2017-01-11T23:52+09:00
################################################################################

## \brief Initialize POSIX shell environment
init(){
	set -eu
	umask 0022
	export LC_ALL='C' PATH="$(command -p getconf PATH):$PATH"
}

is_main()(
	EXE_NAME='.sh'
	CURRENT_EXE="$(ps -p $$ -o comm=)"
	[ "$EXE_NAME" = "$CURRENT_EXE" ]
)

init

parse_arg(){
	for arg; do
		case "$arg" in
			-h|--help) echo "help $opt";;
			-a|--long-a) flag_a="OK";;
			-b*|--long-b*)
				# flag_a="OK"
				case "$arg" in
					--long-b=*) optarg_b="${arg#--long-b}";;
					-b*) optarg_b="${arg#-b}"; shift;;
				esac
				: ${optarg_b:=default}
				;;
			-t*|--long-t*)
				case "$arg" in
					--*=*) optarg_t="${arg#*=}";;
					--*)   optarg_t="$2"; shift;;
					-t*)   optarg_t="$2"
				esac

				flag_a="OK";;
		esac

		## ショートオプションのグループ化対策

	done
}

parse_arg "$@"

