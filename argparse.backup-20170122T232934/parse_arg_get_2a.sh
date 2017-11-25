#!/bin/sh
# \file      parse_arg_get_2a.sh
# \author    SENOO, Ken
# \copyright CC0

## \brief Initialize POSIX shell environment
# set -eu
set -u
umask 0022
export LC_ALL='C' PATH="$(command -p getconf PATH):$PATH"

EXE_NAME='parse_arg_get_2a.sh'

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
		eval optarg_$str=''
	done

	while [ $# != 0 ]; do
		while getopts $OPTSTR opt "$@"; do
			case "$opt$OPTARG" in
				h|-help|-hel|-he|-h)                         opt_h='O';;
				V|-version|-versio|-versi|-vers|-ver|-ve|-v) opt_V='O';;

				"t$OPTARG"|-tag|-tag=*)
					exit_if_missing_long_optarg "$@"
					opt_t='O'
					arg="$OPTARG"
					case "$1" in
						--*=*) arg="${OPTARG#*=}";;
						--*)   arg="$2"; shift;;
						*[!t]t)   arg="$OPTARG"; shfit;;
					esac
					eval optarg_t_$((optargc_t+=1))='$arg'
					;;
				\?*) exit_invalid_short_option "$OPTARG";;
				:*)  exit_missing_short_optarg "$OPTARG";;
				-*)  exit_invalid_long_option "$1";;
				*) echo "other: opt: $opt, OPTARG: $OPTARG";;
			esac
		done

		shift
		## For trailing option and end of option
		[ -z "${1+defined}" ] && break

		## Process --
		case "$1" in --)
			shift
			for arg in "$@"; do
				eval arg_$((argc+=1))='$arg'
			done
			break
		esac

		eval arg_$((argc+=1))='$1'
		shift
	done

	printf "argc:${argc:-0}"
	while [ $((i+=1)) -le ${argc:-0} ]; do
		eval printf '", %s=%s"' "arg_$i" \"\$arg_$i\"
	done

	printf ".\nopt_h:$opt_h, opt_V:$opt_V\n"
	printf "opt_t:$opt_t"

	while [ $((j+=1)) -le ${optargc_t:-0} ]; do
		eval printf '", %s=%s"' "optarg_t_$j" \"\$optarg_t_$j\"
	done
	echo "."
)

if is_main; then
	parse_arg "$@"
fi

