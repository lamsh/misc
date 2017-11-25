#!/bin/sh
# \file      parse_arg_get_1.sh
# \author    SENOO, Ken
# \copyright CC0

## \brief Initialize POSIX shell environment
# set -eu
set -u
umask 0022
export LC_ALL='C' PATH="$(command -p getconf PATH):$PATH"

EXE_NAME='parse_arg_get_1.sh'

is_main()(
	CURRENT_EXE=$(ps -p $$ -o args=)
	case "$CURRENT_EXE" in *$EXE_NAME*);;
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
	echo "$EXE_NAME: option requires an argument -- '$1'" >&2
	exit_try_help
}

## \param[in] $1 $@
exit_if_missing_long_optarg(){
	if [ ${1%%[!-]*} = '--' ] && [ -n "${1##*=*}" ] && [ $# = 1 ]; then
		echo "$EXE_NAME: option '$1' requires an argument" >&2
		exit_try_help
	fi
}


parse_arg()(

	OPTSTR=':-:Vht:'
	for str in $(echo "$OPTSTR" | sed 's/[:-]//g' | fold -w 1); do
		eval opt_$str='X'
	done

	while getopts $OPTSTR opt "$@"; do
		# echo "ECHO opt: $opt, OPTARG: $OPTARG, OPTIND: $OPTIND, @: $@"

		case "$opt$OPTARG" in
			h|-help|-hel|-he|-h)                         opt_h='O';;
			V|-version|-versio|-versi|-vers|-ver|-ve|-v) opt_V='O';;

			"t$OPTARG"|-tag|-tag=*)
				exit_if_missing_long_optarg "$@"
				opt_t='O'
				case "$opt$OPTARG" in
					-*=*) arg="${OPTARG#*=}";;
					-*)   eval arg=\$$OPTIND; OPTIND=$((OPTIND+1));;
					*)    arg="$OPTARG";;
				esac
				eval opt_t_arg$((opt_t_argc+=1))='$arg'
				# opt_t_arg="$arg"
				;;
			\?*) exit_invalid_short_option "$OPTARG";;
			:*)  exit_missing_short_optarg "$OPTARG";;
			-*)  exit_invalid_long_option "$1";;
		esac
	done

	shift $((OPTIND - 1))

	for arg in "$@"; do
		eval arg$((argc+=1))='$arg'
	done

	printf "argc:${argc:-0}"
	while [ $((i+=1)) -le ${argc:-0} ]; do
		eval printf '", %s=%s"' "arg$i" \"\$arg$i\"
	done

	printf ".\nopt_h:$opt_h, opt_V:$opt_V\n"
	printf "opt_t:$opt_t"

	while [ $((j+=1)) -le ${opt_t_argc:-0} ]; do
		eval printf '", %s=%s"' "opt_t_arg$j" \"\$opt_t_arg$j\"
	done
	echo "."
)

if is_main; then
	parse_arg "$@"
fi

