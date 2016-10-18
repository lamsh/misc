#!/bin/sh
# \file      parse_arg.sh
# \author    SENOO, Ken
# \copyright CC0

set -u

readonly PROGNAME=$(basename $0)

usege_exit()(
	cat <<- EOT >&2
	Usage: $PROGNAME [options...] arg1 arg2
	options:
		-h, --help     Show this help
		-V, --version  Show version
		-a, --enable-a Switch on A
		-s
		--long-opt
		-b, --bag[=BAG] Bad tag
		    --long-arg[=olarg]
		-t, --tag=TAG  tag
		    --long-arg=larg
	Example: $PROGNAME --tag=hoge
	EOT
	exit 1
)

argparse()(
	argc=0
	opt_tags=""
	opt_bags=""
	while [ $# != 0 ]
	do
		while getopts ":-:abht:sV" opt
		do
			case "$opt$OPTARG" in
				h|-help) echo "help $opt";;
				V|-version) echo "version $opt";;
				a|-enable-a) echo "flag $opt";;

				## ロングオプションがきたらOPTARGにロングオプション名が入っている
				## $optには"-"が入っている。
				## これを補足してオプションの処理をする
				## ロングオプションの場合はシフトして次の引数をオプション引数とする
				## 引数にリストが来た場合の対処
				## 任意引数ありオプションでリストが来ることはあまりないが一応

				# ショートオプションでは$OPTARGは空

				"b$OPTARG"|-bag*)
					echo "bags: opt: $opt, OPTARG:$OPTARG, \$1: $1 OPTIND: $OPTIND"
					## default
					opt_bags='default'

					# getoptsでは必須引数ありオプションで引数がなかったら?に飛ぶ
					# だから任意引数ありオプションは引数なしオプションとして扱う

					## short option オプション($1)の直後に文字があれば引数とみなしてセット
					[ "$opt" = b ] && [ -n "${1#*b}" ] && opt_bags="${1#*b}"
					
					## $OPTARGに=をもっていたらロングオプションの引数がセット
					case "$OPTARG" in *=*) opt_bags="${1#*=}"; esac

					shift $((OPTIND - 1))
					;;
				"t$OPTARG"|-tag*)
					## ロングオプションの場合はシフトして次の引数をオプション引数とする
					case "$OPTARG" in tag)
						shift $((OPTIND - 1))
						OPTARG=$1
						shift
					esac

					case "$OPTARG" in -*|'')
						echo "$PROGNAME: option requires an argument -- $1" >&2
						exit 1
					esac
					echo "tag: opt: ${opt}, OPTARG: $OPTARG"
					opt_tags="$opt_tags $OPTARG"
					;;
				\?) usage_exit;;
				:*)
					echo "$PROGNAME: option requires an argument -- $1" >&2
					exit 1
					;;
				*) echo "other: opt: ${opt}, OPTARG: $OPTARG";;
			esac
		done

		# echo "1: $1, $@"
		# echo "preshift: OPTIND-1: $((OPTIND - 1)), \$#: $#, 1: $1, \$@: $@"
		argc=$((argc + 1))

		## Process --
		## --はキャッチが難しいので注意。OPTINDのカウントでオプション扱いされている
		case "$(eval echo \$$((OPTIND - 1)))" in --)
		# case "$1" in --)
				shift $((OPTIND - 1))
				# shift
				eval arg_$argc='$@'
				break
		esac

		## getoptsでは単一の-はキャッチできないのでここで処理
		# echo "OPTIND: $OPTIND, 1: $1, @: $@"
		# case "$(eval echo \$$OPTIND)" in -)
		# 		echo "hyphen $OPTIND"
		# 		argc=$((argc - 1))
		# 		shift $OPTIND
		# 		continue
		# esac

		## Point to next operand
		shift $((OPTIND - 1))

		## Skip args count when trailing option exists
		case $# in 0)
			argc=$((argc - 1))
			break
		esac

		if [ "$1" = - ]; then
			## 標準入力があった
			:
			eval arg_$argc='$1'
			# argc=$((argc - 1))
		else
			## Save operand
			eval arg_$argc='$1'
		fi
		# eval "echo arg_$argc: \$arg_$argc"
		shift
		# echo "after args: OPTIND-1: $((OPTIND - 1)), \$#: $#, \$@: $@"
	done

	for i in $(awk "BEGIN{for(i=1; i<=$argc; ++i) print i}")
	do
		eval "echo arg_$i: \$arg_$i"
	done
	echo "opt_tags: $opt_tags"
	echo "opt_bags: $opt_bags"

)

argparse "$@"
# argparse 0 -a -- -at tag 2 3
