#!/bin/sh
################################################################################
## \file      seq.sh
## \author    SENOO, Ken
## \copyright CC0
################################################################################
set -u

seq()(
	readonly HELP_WARN="Try 'seq --help' for more information.\n"
	# case $# in
	# 	1) LAST="$1";;
	# 	2) FIRST="$1" LAST="$2";;
	# 	3) FIRST="$1" INCREMENT="$2" LAST="$3";;
	# 	0) printf "seq: missing operand\n$HELP_WARN"    1>&2; exit 1;;
	# 	*) printf "seq: extra operand '$4'\n$HELP_WARN" 1>&2; exit 1;;
	# esac
	## Set default value
	# : ${FIRST:=1} ${INCREMENT:=1}

	# if [ "$(command -v bc)" ]; then
	# 	echo "for (i=$FIRST; i<=$LAST; i+=$INCREMENT) i" | bc
	# else
	# 	awk -v FIRST=$FIRST -v INCREMENT=$INCREMENT -v LAST=$LAST 'BEGIN{for(i=FIRST; i<=LAST; i+=INCREMENT) print i}'
	# fi

	argv=''
	for arg in "$@";
	do
		case "$arg" in
			-*) # Process option
				case "$arg" in
					'-f'|'--format')
						FMT="$2"
						shift 2
					;;
					'-s'|'--separator')
						SEP="$2"
						shift 2
					;;
			 *)  # Process arguments
				 argv="$argv $arg"
				 shift
				 ;;
		esac
	done

	## Remove heading space
	argv=${argv# }
	argc=$(echo $argv | wc -w)

	## Check wheter valid numeric value
	accuracy=0
	for arg in $argv
	do
		case "$arg" in
			*[^0-9.]*)
				printf "seq: invalid floating point argument: '$arg'\n$HELP_WARN"
				exit 1
				;;
		esac

		## Get numeric accuracy
		target=$([ -z "${arg%%*.*}" ] && printf "${arg##*.}" | wc -c || echo 0)
		[ "$accuracy" -lt "$target" ] && accuracy="$target"
	done

	case "$argc" in
		1)LAST="$argv";;
		2)
			FIRST=$(echo     "$argv" | cut -d " " -f 1)
			LAST=$(echo      "$argv" | cut -d " " -f 2)
			;;
		3)
			FIRST=$(echo     "$argv" | cut -d " " -f 1)
			INCREMENT=$(echo "$argv" | cut -d " " -f 2)
			LAST=$(echo      "$argv" | cut -d " " -f 3)
			;;
		0)printf "seq: missing operand\n$HELP_WARN"    1>&2; exit 1;;
		*)printf "seq: extra operand '$4'\n$HELP_WARN" 1>&2; exit 1;;
	esac

	## Set default value
	: ${FIRST:=1} ${INCREMENT:=1} ${COMPARISON:=<}
	case "$INCREMENT" in -*) COMPARISON='>';; esac

	## Execute seq
		awk "BEGIN{for(i=$FIRST; i$COMPARISON=$LAST; i+=$INCREMENT)
			printf(\"%.${accuracy}f\n\", i)}"
)

seq "$@"
