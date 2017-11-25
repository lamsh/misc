#!/bin/sh
# \file      argparse.sh
# \author    SENOO, Ken
# \copyright CC0

## \brief Initialize POSIX shell environment
set -eu
umask 0022
export LC_ALL='C' PATH="$(command -p getconf PATH):$PATH"

EXE_NAME='argparse.sh'

is_main()(
	NOW_EXE=$(ps -p $$ -o args=)
	case "$NOW_EXE" in *$EXE_NAME*);;
		*) return 1;;
	esac
)

exit_try_help(){
	echo "Try '$EXE_NAME --help' for more information." >&2
	exit 1
}

exit_invalid_short_option(){
	echo "$EXE_NAME: invalid option -- '$OPTARG'" >&2
	exit_try_help
}

exit_invalid_option(){
	echo "$EXE_NAME: unrecognized option '-$opt$OPTARG'" >&2
	exit_try_help
}

exit_missing_short_optarg(){
	echo "$EXE_NAME: option requires an argument -- '$OPTARG'" >&2
	exit_try_help
}

exit_if_missing_long_optarg()(
	ARGC="$1"         # $#
	OPTSTR="$2"  # full --long-option
	if [ $opt = - ] && [ -n "${OPTARG%%*=*}" ] && [ $OPTIND -gt $ARGC ]; then
		echo "$EXE_NAME: option '$OPTSTR' requires an argument" >&2;
		exit_try_help;
	fi
)

exit_if_missing_unconform_optarg()(
	ARGC="$1"  # $#
	if [ $OPTIND -gt $ARGC ]; then
		echo "$EXE_NAME: option '-$opt$OPTARG' requires an argument" >&2
		exit_try_help
	fi
)

validate_numeric_optarg()(
	NARG="$1"
	if [ -z "${NARG%%*[!0-9]*}" ]; then
		echo "$EXE_NAME: invalid number: '$NARG'" >&2
		exit 1
	elif [ "${NARG}" -le 0 ]; then
		echo "$EXE_NAME: invalid number: '$NARG': Numerical result out of range" >&2
		exit 1
	elif [ "$NARG" -gt $((2<<30 - 1)) ] || [ "$NARG" -lt $((-2<<30 + 1)) ]; then
		echo "$EXE_NAME: invalid number: '$NARG': Value too large for defined data type" >&2
		exit 1
	fi
)


argparse()(
	SHIFT_NOW_ARG_TO_1='eval [ $OPTIND -gt 2  ] && shift $((OPTIND-2)) || :'

	OPTSTR=':-:0123456789ahn:p:t:u:V'
	for str in $(echo "$OPTSTR" | sed 's/[:-]//g' | fold -w 1); do
		eval is_opt_$str='false'
		eval opt_${str}_arg=''
		eval opt_${str}_argc=0
	done

	argc=0
	is_opt_U='false'
	opt_U_arg=''

	while [ $# != 0 ]; do
		while getopts $OPTSTR opt; do
			# echo "opt:$opt, OPTARG:$OPTARG, OPTIND:$OPTIND, #:$#, @:$@"
			case "$opt$OPTARG" in
				h|-help|-hel|-he|-h)                         is_opt_h='true';;
				V|-version|-versio|-versi|-vers|-ver|-ve|-v) is_opt_V='true';;
				t*|-tag|-tag=*|-ta|-t|-ta=*|-t=*)
					exit_if_missing_long_optarg $# "--tag"
					is_opt_t='true'
					case "$opt$OPTARG" in
						-*=*) arg="${OPTARG#*=}";;
						-*)   eval arg=\$$OPTIND; OPTIND=$((OPTIND+1));;
						*)    arg="$OPTARG";;
					esac
					eval opt_t_arg$((opt_t_argc+=1))='$arg'
					shift $((OPTIND - 1))
					;;
				a|-any|-any=*|-an|-a|-an=*|-a=*)
					$SHIFT_NOW_ARG_TO_1
					is_opt_a='true'
					case "$1" in
						--*=*) arg="${1#*=}";;
						--*)   arg='';;
						-*)    arg="${1#*$opt}"; shift;;
					esac
					[ -n "$arg" ] && opt_a_arg="$arg" || : ${opt_a_arg:=default}
					;;
				[0-9]|n*|-number|-number=*|\
				-numbe|-numb|-num|-nu|-n|-numbe=*|-numb=*|-num=*|-nu=*|-n=*)
					exit_if_missing_long_optarg $# "--number"
					is_opt_n='true'
					case "$opt$OPTARG" in
						-*=*) arg="${OPTARG#*=}";;
						-*)   eval arg=\$$OPTIND; OPTIND=$((OPTIND+1));;
						$opt)
							$SHIFT_NOW_ARG_TO_1
							## ex: opt=1, -h10V20t10 -> 10V20t10 -> 10
							GET_NUM_FROM_1='eval arg="$opt${1#*$opt}"; arg="${arg%%[!0-9]*}"'
							$GET_NUM_FROM_1
							IS_LAST_ARG='eval [ -z "${1#*$arg}" ]'
							$IS_LAST_ARG && shift || set -- "-${@#*$arg}"
							;;
						*)    arg="$OPTARG";;
					esac
					opt_n_arg="$arg"
					;;
				p*|-plus|-plus=*|-plu|-pl|-p|-plu=*|-pl=*|-p=*)
					exit_if_missing_long_optarg $# "--plus"
					is_opt_p='true'
					case "$opt$OPTARG" in
						-*=*) arg="${OPTARG#*=}";;
						-*)   eval arg=\$$OPTIND; OPTIND=$((OPTIND+1));;
						*)    arg="$OPTARG";;
					esac
					opt_p_arg="$arg"
					shift $((OPTIND-1))
					;;
				unconform) is_opt_u='true';;
				unconform-arg)
					exit_if_missing_unconform_optarg $#
					is_opt_U='true'
					eval opt_U_arg=\$$OPTIND
					shift $OPTIND
					;;
				:u)  exit_invalid_short_option;;
				:*)  exit_missing_short_optarg;;
				\?*) exit_invalid_short_option;;
				*)   exit_invalid_option;;
			esac
		done

		# echo "AFTER: opt:$opt, OPTARG:${OPTARG:-}, OPTIND:$OPTIND, #:$#, @:$@"
		
		## Process --
		GET_NOW_ARG='eval eval printf %s \$$((OPTIND-1))'
		case "$($GET_NOW_ARG)" in --)
			shift $((OPTIND - 1))
			for arg; do
				eval arg$((argc+=1))='$arg'
			done
			break
		esac

		shift $((OPTIND - 1))
		## For trailing option and end of option
		[ $# = 0 ] && break
		## + option
		[ "${1%%[!+]*}" = + ] && set -- "--plus=${@#+}" && continue

		eval arg$((argc+=1))='$1'
		shift
	done

	## Arguments check
	$is_opt_n && validate_numeric_optarg "$opt_n_arg"

	## Show all of now options and operands
	printf "argc:$argc"
	while [ $((i+=1)) -le $argc ]; do
		eval printf '", %s=%s"' "arg$i" \"\$arg$i\"
	done

	printf '.\n'
	printf '%-14s.\n' "is_opt_h:$is_opt_h"
	printf '%-14s.\n' "is_opt_V:$is_opt_V"
	printf '%-14s.\n' "is_opt_u:$is_opt_u"
	printf '%-14s, %s\n' "is_opt_a:$is_opt_a" "opt_a_arg=$opt_a_arg."
	printf '%-14s, %s\n' "is_opt_n:$is_opt_n" "opt_n_arg=$opt_n_arg."
	printf '%-14s, %s\n' "is_opt_U:$is_opt_U" "opt_U_arg=$opt_U_arg."
	printf '%-14s, %s\n' "is_opt_p:$is_opt_p" "opt_p_arg=$opt_p_arg."
	printf '%-14s' "is_opt_t:$is_opt_t"
	while [ $((j+=1)) -le $opt_t_argc ]; do
		eval printf '", %s=%s"' "opt_t_arg$j" \"\$opt_t_arg$j\"
	done
	echo "."
)

if is_main; then
	argparse "${@:-}"
fi
