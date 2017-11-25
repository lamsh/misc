#!/bin/sh
# \file      parse_arg_get_3a.sh
# \author    SENOO, Ken
# \copyright CC0

## \brief Initialize POSIX shell environment
set -eu
umask 0022
export LC_ALL='C' PATH="$(command -p getconf PATH):$PATH"

EXE_NAME='parse_arg_get_3a.sh'

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
EXIT_TRY_HELP="eval
	echo Try \'$EXE_NAME --help\' for more information. >&2;
	exit 1;
"
EXIT_INVALID_SHORT_OPTION="eval
	echo $EXE_NAME: invalid option -- \'\$OPTARG\' >&2;
	exit_try_help
"

EXIT_INVALID_LONG_OPTION="eval
	echo $EXE_NAME: unrecognized option \'-\$opt\$OPTARG\' >&2;
	exit_try_help
"

EXIT_MISSING_SHORT_OPTARG="eval
	echo $EXE_NAME: option requires an argument -- \'\$OPTARG\' >&2;
	exit_try_help
"

## \param[in] $1 $@
exit_if_missing_long_optarg(){
	if [ ${1%%[!-]*} = '--' ] && [ -n "${1##*=*}" ] && [ $# = 1 ]; then
		echo "$EXE_NAME: option '$1' requires an argument" >&2
		exit_try_help
	fi
}
EXIT_IF_MISSING_LONG_OPTARG="eval
	if [ \$OPTIND -gt \$# ]; then
		echo $EXE_NAME: option \'--\$OPTARG\' requires an argument >&2;
		exit_try_help;
	fi
"


parse_arg()(

	OPTSTR=':-:0123456789Vahn:t:u:'
	for str in $(echo "$OPTSTR" | sed 's/[:-]//g' | fold -w 1); do
		eval opt_$str='X'
		eval opt_${str}_arg=''
	done

	while [ $# != 0 ]; do
		while getopts $OPTSTR opt "$@"; do
			echo "opt:$opt, OPTARG:$OPTARG, OPTIND:$OPTIND, #;$#, @:$@"
			case "$opt$OPTARG" in
				h|-help|-hel|-he|-h)                         opt_h='O';;
				V|-version|-versio|-versi|-vers|-ver|-ve|-v) opt_V='O';;

				"t$OPTARG") opt_t='O'; eval opt_t_arg$((opt_t_argc+=1))='$OPTARG';;
				-tag=*|-ta=*|-t=*) opt_t='O'
					eval opt_t_arg$((opt_t_argc+=1))='${OPTARG#*=}';;
				-tag|-ta|-t)
					$EXIT_IF_MISSING_LONG_OPTARG
					opt_t='O'
					eval arg=\$$OPTIND; OPTIND=$((OPTIND+1))
					eval opt_t_arg$((opt_t_argc+=1))='$arg'
					;;
				a) opt_a='O'; opt_a_arg="${1#*$opt}"; shift; : ${opt_a_arg:=default};;
				-any|-an|-a) opt_a='O'; : ${opt_a_arg:=default};;
				-any=*|-an=*|-a=*)
					opt_a='O'
					opt_a_arg="${1#*=}"
					: ${opt_a_arg:=default}
					;;
				[0-9]|"n$OPTARG"|-number|-number=*|\
				-numbe|-numb|-num|-nu|-n|-numbe=*|-numb=*|-num=*|-nu=*|-n=*)
					exit_if_missing_long_optarg "$@"
					opt_n='O'
					case "$opt$OPTARG" in
						-*=*) arg="${OPTARG#*=}";;
						-*)   eval arg=\$$OPTIND; OPTIND=$((OPTIND+1));;
						## -0形式の場合，先頭から数字のグループまで削除して$@の再セット
						[0-9])
							shift $((OPTIND > 2 ? OPTIND-2 : 0))
							## ex: opt=1, -h10V20t10 -> 10a20t10 -> 10
							arg="$opt${1#*$opt}"; arg="${arg%%[!0-9]*}"
							set -- "-${@#*$arg}"
							;;
						*)    arg="$OPTARG";;
					esac

					if [ -z "${arg%%*[!0-9]*}" ]; then
						echo "$EXE_NAME: invalid number: '$arg'" >&2
						exit 1
					fi
					opt_n_arg="$arg"
					;;
				u*|unconform)
					opt_u='O'
					eval opt_u_arg=\$$OPTIND; OPTIND=$((OPTIND+1))
					;;
				-*)  $EXIT_INVALID_LONG_OPTION;;
				:*)  $EXIT_MISSING_SHORT_OPTARG;;
				\?*) $EXIT_INVALID_SHORT_OPTION;;
			esac
		done

		## Process --
		case "$(eval printf %s \"\$$((OPTIND-1))\")" in --)
			shift $((OPTIND -1))
			for arg in "$@"; do
				eval arg$((argc+=1))='$arg'
			done
			break
		esac

		shift $((OPTIND - 1))
		## For trailing option and end of option
		[ -z "${1+defined}" ] && break

		eval arg$((argc+=1))='$1'
		shift
	done

	printf "argc:${argc:-0}"
	while [ $((i+=1)) -le ${argc:-0} ]; do
		eval printf '", %s=%s"' "arg$i" \"\$arg$i\"
	done

	printf ".\nopt_h:$opt_h, opt_V:$opt_V.\n"
	printf "opt_t:$opt_t"

	while [ $((j+=1)) -le ${opt_t_argc:-0} ]; do
		eval printf '", %s=%s"' "opt_t_arg$j" \"\$opt_t_arg$j\"
	done
	echo "."
	echo "opt_a:$opt_a, opt_a_arg=$opt_a_arg."
	echo "opt_n:$opt_n, opt_n_arg=$opt_n_arg."
	echo "opt_u:$opt_u, opt_u_arg=$opt_u_arg."
)

if is_main; then
	parse_arg "$@"
fi

