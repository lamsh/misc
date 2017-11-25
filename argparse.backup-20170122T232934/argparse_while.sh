#!/bin/sh
# \file      argparse_while.sh
# \author    SENOO, Ken
# \copyright CC0

## \brief Initialize POSIX shell environment
set -eu
umask 0022
export LC_ALL='C' PATH="$(command -p getconf PATH):$PATH"

EXE_NAME='argparse_while.sh'

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

## \param[in] $1 OPTARG
exit_invalid_short_option(){
	echo "$EXE_NAME: invalid option -- '$1'" >&2
	exit_try_help
}

## \param[in] $1 $1
exit_invalid_long_option(){
	echo "$EXE_NAME: unrecognized option '$1'" >&2
	exit_try_help
}

## \param[in] $1 OPTARG
exit_missing_short_optarg(){
	if [ -z "${1#*$opt}" ] && [ $# = 1 ]; then
		echo "$EXE_NAME: option requires an argument -- '${1#-}'" >&2
		exit_try_help
	fi
}

exit_if_missing_long_optarg(){
	ARGC=$(($# - 1))
	OPTSTR="$1"  # full --long-option
	NOW_ARG="$2"
	if [ -n "${NOW_ARG%%*=*}" ] && [ $ARGC = 1 ]; then
		echo "$EXE_NAME: option '$OPTSTR' requires an argument" >&2
		exit_try_help
	fi
}

exit_if_missing_unconform_optarg()(
	ARGC=$#;  OPTSTR="$1"  # -unconform option
	if [ $ARGC = 1 ]; then
		echo "$EXE_NAME: option '$OPTSTR' requires an argument" >&2
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
		# echo "ECHO arg:$1, @: $@"
		case "$1" in
			--)
				shift
				for arg in "$@"; do
					eval arg$((argc+=1))='$arg'
				done
				break
				;;
			--help|--hel|--he|--h)                            is_opt_h='true';;
			--version|--versio|--versi|--vers|--ver|--ve|--v) is_opt_V='true';;
			--tag|--tag=*|--ta|--ta|--t|--ta=*|--t=*)
				exit_if_missing_long_optarg '--tag' "$@"
				is_opt_t='true'
				[ -n "${1%%*=*}" ] && arg="$2" && shift || arg="${1#*=}"
				eval opt_t_arg$((opt_t_argc+=1))='$arg'
				;;
			--any|--any=*|--an|--a|--an=*|--a=*)
				is_opt_a='true'
				[ -z "${1%%*=*}" ] && arg="${1#*=}"    || arg=''
				[ -n "$arg"      ] && opt_a_arg="$arg" || : ${opt_a_arg:=default}
				;;
			--number|--number=*|\
			--numbe|--numb|--num|--nu|--n|--numbe=*|--numb=*|--num=*|--nu=*|--n=*)
				exit_if_missing_long_optarg '--number' "$@"
				is_opt_n='true'
				[ -n "${1%%*=*}" ] && arg="$2" && shift || arg="${1#*=}"
				opt_n_arg="$arg"
				;;
			-unconform) is_opt_u='true';;
			-unconform-arg)
				exit_if_missing_unconform_optarg "$@"
				is_opt_U='true'; opt_U_arg="$2"; shift
				;;
			--plus|--plus=*|--plu|--pl|--p|--plu=*|--pl=*|--p=*)
				exit_if_missing_long_optarg '--plus' "$@"
				is_opt_p='true'
				[ -n "${1%%*=*}" ] && arg="$2" && shift || arg="${1#*=}"
				opt_p_arg="$arg"
				;;
			+*) set -- "--plus=${@#+}" && continue;;
			--*) exit_invalid_long_option "$1";;
			--*|-u?*) exit_invalid_long_option "$1";;
			-*)
				for opt in $(echo "${1#-}" | fold -w 1); do
					case $opt in
						h) is_opt_h='true';;
						V) is_opt_V='true';;
						t)
							is_opt_t='true'
							exit_missing_short_optarg "$@"
							[ -n "${1#*$opt}" ] && arg="${1#*$opt}" || { arg="$2"; shift; }
							eval opt_t_arg$((opt_t_argc+=1))='$arg'
							break
							;;
						a)
							is_opt_a='true'
							arg="${1#*$opt}"
							[ -n "$arg" ] && opt_a_arg="$arg" || : ${opt_a_arg:=default}
							break
							;;
						n)
							is_opt_n='true'
							exit_missing_short_optarg "$@"
							[ -n "${1#*$opt}" ] && arg="${1#*$opt}" || { arg="$2"; shift; }
							opt_n_arg="$arg"
							break
							;;
						[0-9])
							is_opt_n='true'
							## ex: opt=1, -h10V20t10 -> 10V20t10 -> 10
							GET_NUM_FROM_1='eval arg="$opt${1#*$opt}"; arg="${arg%%[!0-9]*}"'
							$GET_NUM_FROM_1
							[ $((skip_counter-=1)) -gt 1 ] && continue
							skip_counter=$(echo $arg | wc -m)
							opt_n_arg="$arg"
							IS_LAST_ARG='eval [ -z "${1#*$arg}" ]'
							$IS_LAST_ARG || set -- "-${@#*$arg}"
							;;
						?) exit_invalid_short_option $opt;;
					esac
				done
			;;
			*) eval arg$((argc+=1))='$1';;
		esac
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
	argparse "$@"
fi

